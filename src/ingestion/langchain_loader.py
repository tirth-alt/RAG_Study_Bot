"""
LangChain-based document loading and chunking.
Replaces custom PDF loader and text chunker with LangChain equivalents.
"""

from typing import List, Dict, Union
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class LangChainDocumentProcessor:
    """
    Document loading and chunking using LangChain.
    """
    
    def __init__(self, chunk_size: int = 1200, chunk_overlap: int = 350):
        """
        Initialize the processor.
        
        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len,
        )
    
    def load_pdf(self, pdf_path: Union[str, Path]) -> List[Document]:
        """
        Load PDF using LangChain's PyPDFLoader.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of Document objects with page content and metadata
        """
        loader = PyPDFLoader(str(pdf_path))
        documents = loader.load()
        
        # Add custom metadata (subject from filename)
        pdf_name = Path(pdf_path).stem
        for doc in documents:
            doc.metadata['subject'] = pdf_name
            doc.metadata['filename'] = pdf_name
            
        return documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks using LangChain's text splitter.
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of chunked Document objects with preserved metadata
        """
        chunks = self.text_splitter.split_documents(documents)
        return chunks
    
    def process_pdfs(self, pdf_directory: Union[str, Path]) -> List[Document]:
        """
        Process all PDFs in a directory.
        
        Args:
            pdf_directory: Directory containing PDF files
            
        Returns:
            List of chunked documents with metadata
        """
        pdf_dir = Path(pdf_directory)
        if not pdf_dir.exists():
            raise ValueError(f"Directory not found: {pdf_directory}")
        
        all_chunks = []
        pdf_files = list(pdf_dir.glob("*.pdf"))
        
        if not pdf_files:
            raise ValueError(f"No PDF files found in {pdf_directory}")
        
        print(f"📂 Found {len(pdf_files)} PDF files")
        
        for pdf_path in pdf_files:
            print(f"📄 Loading: {pdf_path.name}")
            
            # Load PDF
            documents = self.load_pdf(pdf_path)
            
            # Chunk documents
            chunks = self.chunk_documents(documents)
            
            print(f"   ✅ Created {len(chunks)} chunks")
            all_chunks.extend(chunks)
        
        print(f"\n✅ Total chunks created: {len(all_chunks)}")
        return all_chunks


# Backward compatibility functions (for existing code)
def load_pdf(pdf_path: str) -> List[Dict]:
    """Load PDF and return chunks in old format."""
    processor = LangChainDocumentProcessor()
    docs = processor.load_pdf(pdf_path)
    chunks = processor.chunk_documents(docs)
    
    # Convert to old format
    return [
        {
            'text': doc.page_content,
            'metadata': doc.metadata
        }
        for doc in chunks
    ]


def load_pdfs_from_directory(directory: str, chunk_size: int = 1200, chunk_overlap: int = 350) -> List[Dict]:
    """Load all PDFs from directory and return chunks in old format."""
    processor = LangChainDocumentProcessor(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = processor.process_pdfs(directory)
    
    # Convert to old format
    return [
        {
            'text': doc.page_content,
            'metadata': doc.metadata
        }
        for doc in chunks
    ]


if __name__ == "__main__":
    # Test the processor
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python langchain_loader.py <pdf_directory>")
        sys.exit(1)
    
    processor = LangChainDocumentProcessor()
    chunks = processor.process_pdfs(sys.argv[1])
    
    # Show sample
    print(f"\n📝 Sample chunk:")
    print(f"Subject: {chunks[0].metadata.get('subject')}")
    print(f"Page: {chunks[0].metadata.get('page')}")
    print(f"Text: {chunks[0].page_content[:200]}...")
