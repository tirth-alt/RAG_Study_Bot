"""
PDF Loader Module
Loads PDF textbooks and extracts text with metadata.
"""

import os
from typing import List, Dict
import fitz  # PyMuPDF
from pathlib import Path


class PDFLoader:
    """Load and extract text from PDF textbooks."""
    
    def __init__(self, pdf_directory: str = "data/raw"):
        """
        Initialize PDF loader.
        
        Args:
            pdf_directory: Directory containing PDF files
        """
        self.pdf_directory = Path(pdf_directory)
        
    def load_pdf(self, pdf_path: str) -> List[Dict[str, any]]:
        """
        Load a single PDF and extract text with metadata.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of dictionaries containing page text and metadata
        """
        documents = []
        
        try:
            # Open PDF
            pdf_document = fitz.open(pdf_path)
            
            # Extract filename and parent directory for subject identification
            pdf_file = Path(pdf_path)
            filename = pdf_file.stem
            parent_dir = pdf_file.parent.name
            
            # Try to identify subject from parent directory first (for chapter-wise PDFs)
            # Then fall back to filename
            subject = self._identify_subject(parent_dir)
            if subject == "Social Science":  # Default wasn't found in parent
                subject = self._identify_subject(filename)
            
            print(f"📖 Loading {filename} ({len(pdf_document)} pages) - Subject: {subject}")
            
            # Extract text from each page
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                text = page.get_text()
                
                # Skip empty pages
                if not text.strip():
                    continue
                
                # Create document with metadata
                doc = {
                    "text": text,
                    "metadata": {
                        "source": filename,
                        "subject": subject,
                        "page": page_num + 1,
                        "total_pages": len(pdf_document)
                    }
                }
                documents.append(doc)
            
            pdf_document.close()
            print(f"✅ Loaded {len(documents)} pages from {filename}")
            
        except Exception as e:
            print(f"❌ Error loading PDF {pdf_path}: {str(e)}")
            raise
            
        return documents
    
    def load_all_pdfs(self) -> List[Dict[str, any]]:
        """
        Load all PDFs from the configured directory.
        
        Returns:
            List of all documents from all PDFs
        """
        all_documents = []
        
        # Find all PDF files (including subdirectories)
        pdf_files = list(self.pdf_directory.rglob("*.pdf"))
        
        if not pdf_files:
            print(f"⚠️  No PDF files found in {self.pdf_directory}")
            return all_documents
        
        print(f"\n🔍 Found {len(pdf_files)} PDF file(s)")
        
        # Load each PDF
        for pdf_file in pdf_files:
            docs = self.load_pdf(str(pdf_file))
            all_documents.extend(docs)
        
        print(f"\n📚 Total documents loaded: {len(all_documents)}")
        return all_documents
    
    def _identify_subject(self, filename: str) -> str:
        """
        Identify subject from filename or parent directory.
        
        Args:
            filename: PDF filename
            
        Returns:
            Subject name
        """
        filename_lower = filename.lower()
        
        # Check for subject keywords in filename or path
        if "english" in filename_lower:
            return "English"
        elif "social" in filename_lower or "sst" in filename_lower:
            return "Social Science"
        elif "history" in filename_lower:
            return "History"
        elif "polity" in filename_lower or "civics" in filename_lower or "politics" in filename_lower:
            return "Polity"
        elif "economics" in filename_lower or "econ" in filename_lower:
            return "Economics"
        elif "geography" in filename_lower or "geo" in filename_lower:
            return "Geography"
        else:
            return "Social Science"  # Default for CBSE Class 10


if __name__ == "__main__":
    # Test the loader
    loader = PDFLoader()
    documents = loader.load_all_pdfs()
    
    if documents:
        print(f"\n📄 Sample document:")
        print(f"Subject: {documents[0]['metadata']['subject']}")
        print(f"Page: {documents[0]['metadata']['page']}")
        print(f"Text preview: {documents[0]['text'][:200]}...")
