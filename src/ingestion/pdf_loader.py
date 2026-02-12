"""
PDF Loader Module
Handles loading and processing of PDF textbooks with metadata extraction.
"""

import os
import re
from pathlib import Path
from typing import List, Dict
import fitz  # PyMuPDF


class PDFLoader:
    """Load and extract text from PDF files."""
    
    def __init__(self, pdf_directory: str = "data/raw"):
        """
        Initialize PDF loader.
        
        Args:
            pdf_directory: Directory containing PDF files
        """
        self.pdf_directory = Path(pdf_directory)
        
    def _extract_chapter_info(self, text: str, page_num: int, filename: str) -> Dict[str, str]:
        """
        Extract chapter information from text.
        
        Args:
            text: Page text
            page_num: Page number
            filename: PDF filename
            
        Returns:
            Dictionary with chapter_number and chapter_name
        """
        chapter_info = {"number": None, "name": None}
        
        # Only check first few pages
        if page_num > 5:
            return chapter_info
        
        # Patterns to match chapter headers
        patterns = [
            r'Chapter\s+(\d+)[:\s]+(.+?)(?:\n|$)',  # Chapter 1: Title
            r'CHAPTER\s+(\d+)[:\s]+(.+?)(?:\n|$)',  # CHAPTER 1: TITLE
            r'Ch(?:apter)?\s*\.?\s*(\d+)[:\s]+(.+?)(?:\n|$)',  # Ch. 1: Title
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                chapter_num = match.group(1)
                chapter_name = match.group(2).strip()[:100]
                
                # Validate: chapter numbers should be 1-20 (reject years like 2007)
                if chapter_num.isdigit() and 1 <= int(chapter_num) <= 20:
                    chapter_info["number"] = chapter_num
                    chapter_info["name"] = chapter_name
                    break
        
        return chapter_info
        
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
            
            # Try to extract chapter info from first few pages
            chapter_info = None
            for page_num in range(min(3, len(pdf_document))):
                page = pdf_document[page_num]
                text = page.get_text()
                chapter_info = self._extract_chapter_info(text, page_num, filename)
                if chapter_info["number"]:
                    break
            
            # Extract text from each page
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                text = page.get_text()
                
                # Skip empty pages
                if not text.strip():
                    continue
                
                # Create document with enriched metadata
                doc = {
                    "text": text,
                    "metadata": {
                        "source": filename,
                        "subject": subject,
                        "page": page_num + 1,
                        "total_pages": len(pdf_document),
                        "chapter_number": chapter_info.get("number") if chapter_info else None,
                        "chapter_name": chapter_info.get("name") if chapter_info else None
                    }
                }
                documents.append(doc)
            
            pdf_document.close()
            if chapter_info and chapter_info.get("number"):
                print(f"✅ Loaded {len(documents)} pages from {filename} (Chapter {chapter_info['number']})")
            else:
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
        
        print(f"\\n📚 Found {len(pdf_files)} PDF files")
        print("="*60)
        
        for pdf_file in pdf_files:
            try:
                documents = self.load_pdf(str(pdf_file))
                all_documents.extend(documents)
            except Exception as e:
                print(f"⚠️  Skipping {pdf_file.name} due to error: {str(e)}")
                continue
        
        print("="*60)
        print(f"✅ Loaded {len(all_documents)} total pages from {len(pdf_files)} PDFs\\n")
        
        return all_documents
    
    def _identify_subject(self, text: str) -> str:
        """
        Identify subject from filename or directory name.
        
        Args:
            text: Filename or directory name
            
        Returns:
            Subject name
        """
        text_lower = text.lower()
        
        # Check for specific subjects
        if any(keyword in text_lower for keyword in ['history', 'bharat', 'india']):
            return "History"
        elif any(keyword in text_lower for keyword in ['polity', 'civics', 'political', 'democracy', 'constitution']):
            return "Polity"
        elif any(keyword in text_lower for keyword in ['economics', 'economy', 'economic']):
            return "Economics"
        elif any(keyword in text_lower for keyword in ['geography', 'geo', 'jess']):
            return "Geography"
        elif any(keyword in text_lower for keyword in ['english', 'literature', 'first flight', 'footprints']):
            return "English"
        
        # Default to Social Science if no specific match
        return "Social Science"


if __name__ == "__main__":
    # Test PDF loader
    loader = PDFLoader()
    
    documents = loader.load_all_pdfs()
    
    if documents:
        # Show sample
        print(f"\\n📝 Sample document:")
        print(f"Subject: {documents[0]['metadata']['subject']}")
        print(f"Source: {documents[0]['metadata']['source']}")
        print(f"Chapter: {documents[0]['metadata'].get('chapter_number', 'N/A')}")
        print(f"Page: {documents[0]['metadata']['page']}")
        print(f"Text preview: {documents[0]['text'][:200]}...")
