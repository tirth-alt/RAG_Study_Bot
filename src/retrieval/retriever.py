"""
Retriever Module
Handles query-to-context retrieval pipeline.
"""

from typing import List, Dict, Optional
import numpy as np
from src.vectorstore.embeddings import EmbeddingGenerator
from src.vectorstore.chroma_db import ChromaDBManager


class Retriever:
    """Retrieve relevant context for queries."""
    
    def __init__(self, embedding_generator: EmbeddingGenerator, 
                 chroma_db: ChromaDBManager, top_k: int = 3):
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
    
    def get_context_string(self, query: str, subject_filter: Optional[str] = None) -> tuple:
        """
        Get formatted context string for LLM.
        
        Args:
            query: User query
            subject_filter: Optional subject filter
            
        Returns:
            Tuple of (context_string, sources_list)
        """
        # Retrieve relevant chunks
        results = self.retrieve(query, subject_filter)
        
        if not results["contexts"]:
            return "No relevant information found in the textbook.", []
        
        # Build context string
        context_parts = []
        sources = []
        
        for i, (text, metadata) in enumerate(zip(results["contexts"], results["metadatas"])):
            source_info = f"{metadata.get('subject', 'Unknown')} - {metadata.get('source', 'Unknown')} (Page {metadata.get('page', '?')})"
            
            context_parts.append(f"[Source {i + 1}: {source_info}]\n{text}\n")
            sources.append(source_info)
        
        context_string = "\n".join(context_parts)
        
        return context_string, sources


if __name__ == "__main__":
    # Test retriever (requires existing vector database)
    from src.vectorstore.embeddings import EmbeddingGenerator
    from src.vectorstore.chroma_db import ChromaDBManager
    
    # Initialize components
    embedder = EmbeddingGenerator()
    db = ChromaDBManager()
    retriever = Retriever(embedder, db, top_k=3)
    
    # Test query
    test_query = "What is democracy?"
    
    print(f"\n🔍 Searching for: '{test_query}'")
    
    if db.get_stats()["document_count"] > 0:
        context, sources = retriever.get_context_string(test_query)
        
        print(f"\n📚 Retrieved Context:")
        print(context)
        
        print(f"\n📖 Sources:")
        for source in sources:
            print(f"  - {source}")
    else:
        print("⚠️  No documents in database yet. Run setup first!")
