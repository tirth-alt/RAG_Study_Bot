"""
ChromaDB Module
Manages vector database operations.
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import numpy as np


class ChromaDBManager:
    """Manage ChromaDB vector store."""
    
    def __init__(self, persist_directory: str = "./vectorstore", collection_name: str = "cbse_class10_textbooks"):
        """
        Initialize ChromaDB manager.
        
        Args:
            persist_directory: Directory to persist the database
            collection_name: Name of the collection
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize ChromaDB client
        print(f"🗄️  Initializing ChromaDB at {persist_directory}...")
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "CBSE Class 10 textbooks for English and Social Science"}
        )
        
        print(f"✅ ChromaDB initialized with collection: {collection_name}")
        print(f"📊 Current collection size: {self.collection.count()} documents")
    
    def add_documents(self, chunks: List[Dict[str, any]], embeddings: np.ndarray):
        """
        Add documents to the vector store.
        
        Args:
            chunks: List of text chunks with metadata
            embeddings: Corresponding embeddings
        """
        print(f"\n💾 Adding {len(chunks)} documents to ChromaDB...")
        
        # Prepare data for ChromaDB
        ids = [f"doc_{i}" for i in range(len(chunks))]
        texts = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        
        # Clean metadata: ChromaDB doesn't accept None values
        cleaned_metadatas = []
        for metadata in metadatas:
            cleaned = {}
            for key, value in metadata.items():
                # Convert None to empty string, keep other values
                if value is None:
                    cleaned[key] = ""
                else:
                    cleaned[key] = str(value) if not isinstance(value, (str, int, float, bool)) else value
            cleaned_metadatas.append(cleaned)
        
        # Convert numpy array to list for ChromaDB
        embeddings_list = embeddings.tolist()
        
        # Add to collection in batches
        batch_size = 500
        for i in range(0, len(chunks), batch_size):
            end_idx = min(i + batch_size, len(chunks))
            
            self.collection.add(
                ids=ids[i:end_idx],
                documents=texts[i:end_idx],
                embeddings=embeddings_list[i:end_idx],
                metadatas=cleaned_metadatas[i:end_idx]
            )
            
            print(f"  Batch {i // batch_size + 1}: Added documents {i + 1} to {end_idx}")
        
        print(f"✅ Successfully added all documents")
        print(f"📊 Total documents in collection: {self.collection.count()}")
    
    def search(self, query_embedding: np.ndarray, top_k: int = 3, 
               subject_filter: Optional[str] = None) -> Dict:
        """
        Search for similar documents.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            subject_filter: Optional subject filter
            
        Returns:
            Dictionary with search results
        """
        # Convert numpy array to list
        query_embedding_list = query_embedding.tolist()
        
        # Prepare filter if subject specified
        where_filter = None
        if subject_filter:
            where_filter = {"subject": subject_filter}
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding_list],
            n_results=top_k,
            where=where_filter
        )
        
        return results
    
    def clear_collection(self):
        """Clear all documents from the collection."""
        print(f"🗑️  Clearing collection: {self.collection_name}...")
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"description": "CBSE Class 10 textbooks for English and Social Science"}
        )
        print(f"✅ Collection cleared")
    
    def get_stats(self) -> Dict:
        """
        Get statistics about the collection.
        
        Returns:
            Dictionary with statistics
        """
        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "document_count": count,
            "persist_directory": self.persist_directory
        }


if __name__ == "__main__":
    # Test ChromaDB
    db = ChromaDBManager()
    
    # Print stats
    stats = db.get_stats()
    print(f"\n📊 Database Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
