"""
Setup Script
One-time setup to process PDFs and create vector database.
"""

import os
import sys
import yaml
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ingestion.pdf_loader import PDFLoader
from src.ingestion.text_chunker import TextChunker
from src.vectorstore.embeddings import EmbeddingGenerator
from src.vectorstore.chroma_db import ChromaDBManager


def load_config():
    """Load configuration from YAML file."""
    config_path = "config/config.yaml"
    
    if not os.path.exists(config_path):
        print(f"❌ Configuration file not found: {config_path}")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def check_pdfs():
    """Check if PDF files exist."""
    pdf_dir = Path("data/raw")
    
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        print("Please create the directory and add your textbook PDFs.")
        return False
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in {pdf_dir}")
        print("\nPlease add your CBSE Class 10 textbooks:")
        print("  • English textbook (e.g., english.pdf)")
        print("  • Social Science textbook (e.g., social_science.pdf)")
        return False
    
    print(f"✅ Found {len(pdf_files)} PDF file(s):")
    for pdf in pdf_files:
        print(f"  • {pdf.name}")
    
    return True


def main():
    """Run setup process."""
    print("="*60)
    print("  CBSE Class 10 AI Tutor - Setup")
    print("="*60)
    
    # Load configuration
    print("\n📋 Loading configuration...")
    config = load_config()
    print("✅ Configuration loaded")
    
    # Check for PDFs
    print("\n📚 Checking for PDF files...")
    if not check_pdfs():
        sys.exit(1)
    
    # Ask for confirmation
    print("\n" + "="*60)
    print("This setup will:")
    print("  1. Load and process all PDFs from data/raw/")
    print("  2. Generate embeddings using sentence-transformers")
    print("  3. Create ChromaDB vector database")
    print("  4. This may take a few minutes depending on PDF size")
    print("="*60)
    
    response = input("\nProceed with setup? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Setup cancelled.")
        sys.exit(0)
    
    print("\n" + "="*60)
    print("Starting setup process...")
    print("="*60)
    
    # Step 1: Load PDFs
    print("\n[1/4] Loading PDFs...")
    loader = PDFLoader(pdf_directory="data/raw")
    documents = loader.load_all_pdfs()
    
    if not documents:
        print("❌ No documents loaded. Please check your PDFs.")
        sys.exit(1)
    
    # Step 2: Chunk documents
    print("\n[2/4] Chunking documents...")
    chunker = TextChunker(
        chunk_size=config['chunking']['chunk_size'],
        chunk_overlap=config['chunking']['chunk_overlap']
    )
    chunks = chunker.chunk_documents(documents)
    
    # Step 3: Generate embeddings
    print("\n[3/4] Generating embeddings...")
    print("⏳ This may take a few minutes (first-time model download)...")
    
    embedder = EmbeddingGenerator(
        model_name=config['embedding']['model_name'],
        device=config['embedding']['device']
    )
    
    # Extract text from chunks
    chunk_texts = [chunk["text"] for chunk in chunks]
    embeddings = embedder.generate_embeddings(chunk_texts)
    
    # Step 4: Create vector database
    print("\n[4/4] Creating vector database...")
    
    # Initialize ChromaDB (clear if exists)
    db = ChromaDBManager(
        persist_directory=config['vectorstore']['persist_directory'],
        collection_name=config['vectorstore']['collection_name']
    )
    
    # Clear existing data
    if db.get_stats()["document_count"] > 0:
        print("⚠️  Existing database found. Clearing...")
        db.clear_collection()
    
    # Add documents
    db.add_documents(chunks, embeddings)
    
    # Print final stats
    print("\n" + "="*60)
    print("✅ Setup Complete!")
    print("="*60)
    
    stats = db.get_stats()
    print(f"\n📊 Database Statistics:")
    print(f"  • Collection: {stats['collection_name']}")
    print(f"  • Total chunks: {stats['document_count']}")
    print(f"  • Storage location: {stats['persist_directory']}")
    
    print(f"\n📚 Documents processed:")
    subjects = {}
    for chunk in chunks:
        subject = chunk['metadata']['subject']
        subjects[subject] = subjects.get(subject, 0) + 1
    
    for subject, count in subjects.items():
        print(f"  • {subject}: {count} chunks")
    
    print("\n" + "="*60)
    print("🚀 You're ready to start learning!")
    print("Run: python main.py")
    print("="*60)


if __name__ == "__main__":
    main()
