"""
Text Chunker Module
Splits documents into smaller chunks for embedding.
"""

from typing import List, Dict
import re


class TextChunker:
    """Split text into manageable chunks with overlap."""
    
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 200):
        """
        Initialize text chunker.
        
        Args:
            chunk_size: Target size of each chunk in characters
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    def chunk_documents(self, documents: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """
        Chunk all documents.
        
        Args:
            documents: List of documents with text and metadata
            
        Returns:
            List of chunked documents
        """
        chunked_docs = []
        
        print(f"\n✂️  Chunking {len(documents)} documents...")
        print(f"Chunk size: {self.chunk_size} chars, Overlap: {self.chunk_overlap} chars")
        
        for doc in documents:
            chunks = self._chunk_text(doc["text"], doc["metadata"])
            chunked_docs.extend(chunks)
        
        print(f"✅ Created {len(chunked_docs)} chunks")
        return chunked_docs
    
    def _chunk_text(self, text: str, metadata: Dict) -> List[Dict[str, any]]:
        """
        Split a single text into chunks.
        
        Args:
            text: Text to chunk
            metadata: Metadata to attach to each chunk
            
        Returns:
            List of chunks with metadata
        """
        # Clean text
        text = self._clean_text(text)
        
        if len(text) == 0:
            return []
        
        chunks = []
        start = 0
        chunk_num = 0
        
        while start < len(text):
            # Calculate end position
            end = start + self.chunk_size
            
            # If not at the end, try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings near the chunk boundary
                sentence_end = self._find_sentence_boundary(text, end)
                if sentence_end != -1:
                    end = sentence_end
            
            # Extract chunk
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                # Create chunk with metadata
                chunk = {
                    "text": chunk_text,
                    "metadata": {
                        **metadata,
                        "chunk_num": chunk_num,
                        "chunk_size": len(chunk_text)
                    }
                }
                chunks.append(chunk)
                chunk_num += 1
            
            # Move to next chunk with overlap
            start = end - self.chunk_overlap
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """
        Clean text by removing extra whitespace.
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        # Replace multiple whitespace with single space
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        return text
    
    def _find_sentence_boundary(self, text: str, position: int, window: int = 100) -> int:
        """
        Find the nearest sentence boundary near the position.
        
        Args:
            text: Full text
            position: Target position
            window: Search window size
            
        Returns:
            Position of sentence boundary, or -1 if not found
        """
        # Define sentence endings
        sentence_endings = ['. ', '! ', '? ', '.\n', '!\n', '?\n']
        
        # Search window around the position
        search_start = max(0, position - window)
        search_end = min(len(text), position + window)
        search_text = text[search_start:search_end]
        
        # Find all sentence endings in the window
        best_pos = -1
        best_distance = float('inf')
        
        for ending in sentence_endings:
            pos = search_text.rfind(ending)
            if pos != -1:
                actual_pos = search_start + pos + len(ending)
                distance = abs(actual_pos - position)
                if distance < best_distance:
                    best_distance = distance
                    best_pos = actual_pos
        
        return best_pos


if __name__ == "__main__":
    # Test the chunker
    sample_text = """This is the first sentence. This is the second sentence. 
    This is a paragraph with multiple sentences. It should be split properly. 
    The chunker should respect sentence boundaries when possible."""
    
    chunker = TextChunker(chunk_size=50, chunk_overlap=10)
    
    sample_doc = {
        "text": sample_text,
        "metadata": {"source": "test", "page": 1}
    }
    
    chunks = chunker.chunk_documents([sample_doc])
    
    print(f"\nCreated {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i + 1}: {chunk['text'][:100]}...")
