"""
LangChain-compatible ChromaDB vector store.
Wraps existing ChromaDB with LangChain's Chroma class for unified interface.
"""

from typing import List, Dict, Optional, Any
from langchain_chroma import Chroma
from langchain.embeddings.base import Embeddings
from langchain.schema import Document
import numpy as np


class HuggingFaceEmbeddingsWrapper(Embeddings):
    """
    Wrapper for sentence-transformers embeddings to work with LangChain.
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: str = "cpu"):
        """
        Initialize embeddings model.
        
        Args:
            model_name: Name of the sentence-transformers model
            device: Device to run on ('cpu' or 'cuda')
        """
        from sentence_transformers import SentenceTransformer
        
        print(f"🔄 Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.model.to(device)
        print(f"✅ Model loaded on {device}")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embeddings
        """
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query.
        
        Args:
            text: Query text
            
        Returns:
            Embedding vector
        """
        embedding = self.model.encode([text], convert_to_numpy=True)[0]
        return embedding.tolist()


class LangChainChromaStore:
    """
    LangChain-based ChromaDB vector store manager.
    """
    
    def __init__(
        self,
        persist_directory: str = "./vectorstore",
        collection_name: str = "cbse_class10_textbooks",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        device: str = "cpu"
    ):
        """
        Initialize LangChain Chroma store.
        
        Args:
            persist_directory: Directory to persist the database
            collection_name: Name of the collection
            embedding_model: Embedding model name
            device: Device to run on
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddingsWrapper(
            model_name=embedding_model,
            device=device
        )
        
        # Initialize or load Chroma
        print(f"🗄️  Initializing ChromaDB at {persist_directory}...")
        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )
        
        # Get count
        collection_count = len(self.vectorstore.get()['ids'])
        print(f"✅ ChromaDB initialized with collection: {collection_name}")
        print(f"📊 Current collection size: {collection_count} documents")
    
    def similarity_search(
        self,
        query: str,
        k: int = 7,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Search for similar documents.
        
        Args:
            query: Query text
            k: Number of results to return
            filter: Optional metadata filter
            
        Returns:
            List of similar documents
        """
        return self.vectorstore.similarity_search(
            query,
            k=k,
            filter=filter
        )
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 7,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[tuple[Document, float]]:
        """
        Search with similarity scores.
        
        Args:
            query: Query text
            k: Number of results
            filter: Optional metadata filter
            
        Returns:
            List of (document, score) tuples
        """
        return self.vectorstore.similarity_search_with_score(
            query,
            k=k,
            filter=filter
        )
    
    def as_retriever(self, **kwargs):
        """
        Get LangChain retriever interface.
        
        Args:
            **kwargs: Arguments for retriever (search_type, search_kwargs, etc.)
            
        Returns:
            LangChain retriever
        """
        return self.vectorstore.as_retriever(**kwargs)
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of document IDs
        """
        return self.vectorstore.add_documents(documents)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dictionary with stats
        """
        data = self.vectorstore.get()
        return {
            "collection_name": self.collection_name,
            "document_count": len(data['ids']),
            "persist_directory": self.persist_directory
        }


# Backward compatibility
class ChromaDBManager:
    """
    Legacy interface wrapper for backward compatibility.
    Delegates to LangChainChromaStore.
    """
    
    def __init__(self, persist_directory: str = "./vectorstore", collection_name: str = "cbse_class10_textbooks"):
        self.store = LangChainChromaStore(
            persist_directory=persist_directory,
            collection_name=collection_name
        )
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
        """Legacy search interface."""
        # For now, just return empty to maintain compatibility
        # This will be replaced by LangChain retrieval
        return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        return self.store.get_stats()


if __name__ == "__main__":
    # Test the LangChain store
    store = LangChainChromaStore()
    
    print(f"\n📊 Stats: {store.get_stats()}")
    
    # Test search
    results = store.similarity_search("What is democracy?", k=3)
    
    print(f"\n🔍 Search results:")
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc.page_content[:100]}...")
        print(f"   Metadata: {doc.metadata}\n")
