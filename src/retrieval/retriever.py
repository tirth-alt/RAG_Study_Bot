"""
Retriever Module
Handles query-to-context retrieval pipeline.
"""

from typing import List, Dict, Optional, Tuple
import numpy as np
from src.vectorstore.embeddings import EmbeddingGenerator
from src.vectorstore.chroma_db import ChromaDBManager


class Retriever:
    """Retrieve relevant context for queries."""
    
    def __init__(self, embedding_generator: EmbeddingGenerator, 
                 chroma_db: ChromaDBManager, top_k: int = 5):
        """
        Initialize retriever.
        
        Args:
            embedding_generator: Embedding generator instance
            chroma_db: ChromaDB manager instance
            top_k: Number of chunks to retrieve
        """
        self.embedding_generator = embedding_generator
        self.chroma_db = chroma_db
        self.top_k = top_k
        
    def retrieve(self, query: str, subject_filter: Optional[str] = None) -> Dict:
        """
        Retrieve relevant context for a query.
        
        Args:
            query: User query
            subject_filter: Optional subject filter ("English" or "Social Science")
            
        Returns:
            Dictionary with retrieved chunks and metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_generator.generate_embedding(query)
        
        # Search in vector database
        results = self.chroma_db.search(
            query_embedding=query_embedding,
            top_k=self.top_k,
            subject_filter=subject_filter
        )
        
        # Format results
        formatted_results = self._format_results(results)
        
        return formatted_results
    
    def _format_results(self, results: Dict) -> Dict:
        """
        Format search results for easy consumption.
        
        Args:
            results: Raw ChromaDB results
            
        Returns:
            Formatted results dictionary
        """
        if not results or not results['documents'][0]:
            return {
                "contexts": [],
                "metadatas": [],
                "distances": []
            }
        
        # Extract data from ChromaDB results
        documents = results['documents'][0]
        metadatas = results['metadatas'][0] if 'metadatas' in results else []
        distances = results['distances'][0] if 'distances' in results else []
        
        return {
            "contexts": documents,
            "metadatas": metadatas,
            "distances": distances
        }
    
    
    def _rerank_by_page_number(self, results: Dict, prefer_early: bool = True) -> Dict:
        """
        Rerank results based on page numbers.
        
        Args:
            results: Retrieval results
            prefer_early: If True, prefer early pages (for 'first chapters' queries)
            
        Returns:
            Reranked results
        """
        if not results["contexts"] or not results["metadatas"]:
            return results
        
        # Create list of (index, page_num) tuples
        indexed_results = []
        for i, metadata in enumerate(results["metadatas"]):
            page_num = metadata.get("page", 999)  # Default high if missing
            indexed_results.append((i, page_num))
        
        # Sort by page number (ascending for early, descending for late)
        indexed_results.sort(key=lambda x: x[1], reverse=not prefer_early)
        
        # Take top 50% by page position, rest by original ranking
        cutoff = len(indexed_results) // 2
        
        # Reorder: first half by page number, second half keep original
        reordered_indices = [x[0] for x in indexed_results[:cutoff]]
        reordered_indices += [i for i in range(len(indexed_results)) if i not in reordered_indices]
        
        # Rebuild results in new order
        reranked = {
            "contexts": [results["contexts"][i] for i in reordered_indices],
            "metadatas": [results["metadatas"][i] for i in reordered_indices],
            "distances": [results["distances"][i] for i in reordered_indices] if results["distances"] else []
        }
        
        return reranked
    
    def _expand_query(self, query: str) -> str:
        """
        Expand query with related terms for better retrieval.
        Especially helpful for structural questions.
        
        Args:
            query: Original query
            
        Returns:
            Expanded query
        """
        query_lower = query.lower()
        
        # Detect structural questions about chapters
        if any(phrase in query_lower for phrase in ['first', 'initial', 'beginning']):
            if 'chapter' in query_lower:
                # Add TOC-related terms
                query += " table of contents chapter list introduction"
        
        # Detect chapter-specific queries
        if 'chapter' in query_lower:
            # Extract chapter number if present
            import re
            match = re.search(r'chapter\s*(\d+)', query_lower)
            if match:
                ch_num = match.group(1)
                query += f" chapter {ch_num} Ch. {ch_num} Ch {ch_num}"
        
        return query
    
    def reformulate_query(self, query: str, chat_history: List[Tuple[str, str]] = None) -> str:
        """
        Reformulate query using conversation context for better retrieval.
        
        Args:
            query: Current user query
            chat_history: List of (question, answer) tuples from recent conversation
            
        Returns:
            Reformulated query with context
        """
        if not chat_history or len(chat_history) == 0:
            return query
        
        # Get last Q&A for context
        last_question, last_answer = chat_history[-1]
        
        # Add context to query for better retrieval
        reformulated = f"Previous context: {last_question}\nCurrent question: {query}"
        
        return reformulated
    
    def _detect_subject_from_query(self, query: str) -> Optional[str]:
        """
        Detect subject from user query for automatic filtering.
        
        Args:
            query: User's question
            
        Returns:
            Subject name if detected, None otherwise
        """
        query_lower = query.lower()
        
        # Subject keyword mappings
        if any(word in query_lower for word in ['history', 'historical', 'bharat']):
            return "History"
        elif any(word in query_lower for word in ['polity', 'civics', 'political', 'democracy', 'constitution', 'government']):
            return "Polity"
        elif any(word in query_lower for word in ['economics', 'economy', 'economic', 'money', 'gdp']):
            return "Economics"
        elif any(word in query_lower for word in ['geography', 'geographical', 'resources', 'minerals', 'agriculture']):
            return "Geography"
        elif any(word in query_lower for word in ['english', 'literature', 'poem', 'story', 'grammar']):
            return "English"
        
        return None
    
    def get_context_string(self, query: str, subject_filter: Optional[str] = None,
                           chat_history: List[Tuple[str, str]] = None) -> Tuple[str, List[str]]:
        """
        Get formatted context string for LLM.
        
        Args:
            query: User query
            subject_filter: Optional subject filter
            chat_history: Optional conversation history for query reformulation
            
        Returns:
            Tuple of (context_string, sources_list)
        """
        # Auto-detect subject from query if not explicitly provided
        if subject_filter is None:
            subject_filter = self._detect_subject_from_query(query)
            if subject_filter:
                print(f"🔍 Auto-detected subject: {subject_filter}")
        
        # Expand query for better retrieval (especially structural questions)
        expanded_query = self._expand_query(query)
        
        # Reformulate query if we have conversation context
        search_query = self.reformulate_query(expanded_query, chat_history) if chat_history else expanded_query
        
        # Retrieve relevant chunks
        results = self.retrieve(search_query, subject_filter)
        
        # Apply page-aware reranking for structural queries
        if any(word in query.lower() for word in ['first', 'initial', 'beginning', 'start']):
            results = self._rerank_by_page_number(results, prefer_early=True)
        
        if not results["contexts"]:
            return "No relevant information found in the textbook.", []
        
        # Build context string
        context_parts = []
        sources = []
        
        for i, (text, metadata) in enumerate(zip(results["contexts"], results["metadatas"])):
            source_info = f"{metadata.get('subject', 'Unknown')} - {metadata.get('source', 'Unknown')} (Page {metadata.get('page', '?')})"
            
            context_parts.append(f"[Source {i + 1}: {source_info}]\\n{text}\\n")
            sources.append(metadata)  # Return dict for API
        
        context_string = "\\n".join(context_parts)
        
        return context_string, sources


if __name__ == "__main__":
    # Test retriever (requires existing vector database)
    from src.vectorstore.embeddings import EmbeddingGenerator
    from src.vectorstore.chroma_db import ChromaDBManager
    
    # Initialize components
    embedder = EmbeddingGenerator()
    db = ChromaDBManager()
    retriever = Retriever(embedder, db, top_k=5)
    
    # Test query
    test_query = "What is democracy?"
    
    print(f"\\n🔍 Searching for: '{test_query}'")
    
    if db.get_stats()["document_count"] > 0:
        context, sources = retriever.get_context_string(test_query)
        
        print(f"\\n📚 Retrieved Context:")
        print(context)
        
        print(f"\\n📖 Sources:")
        for source in sources:
            print(f"  - {source}")
    else:
        print("⚠️  No documents in database yet. Run setup first!")
