"""
Embeddings Module
Generates embeddings using sentence-transformers.
"""

from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingGenerator:
    """Generate embeddings for text chunks."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: str = "cpu"):
        """
        Initialize embedding generator.
        
        Args:
            model_name: Name of the sentence-transformers model
            device: Device to run on ("cpu" or "cuda")
        """
        print(f"🔄 Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name, device=device)
        print(f"✅ Model loaded on {device}")
        
    def generate_embeddings(self, texts: List[str], show_progress: bool = True) -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings
            show_progress: Whether to show progress bar
            
        Returns:
            Numpy array of embeddings
        """
        print(f"\n🔢 Generating embeddings for {len(texts)} chunks...")
        
        embeddings = self.model.encode(
            texts,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        
        print(f"✅ Generated embeddings with shape {embeddings.shape}")
        return embeddings
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text string
            
        Returns:
            Numpy array embedding
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings.
        
        Returns:
            Embedding dimension
        """
        return self.model.get_sentence_embedding_dimension()


if __name__ == "__main__":
    # Test the embedding generator
    generator = EmbeddingGenerator()
    
    sample_texts = [
        "What is democracy?",
        "Democracy is a form of government.",
        "The people elect their representatives."
    ]
    
    # Generate embeddings
    embeddings = generator.generate_embeddings(sample_texts, show_progress=False)
    
    print(f"\nEmbedding dimension: {generator.get_embedding_dimension()}")
    print(f"Generated {len(embeddings)} embeddings")
    print(f"Sample embedding shape: {embeddings[0].shape}")
