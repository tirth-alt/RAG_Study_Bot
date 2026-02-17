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

from src.ingestion.langchain_loader import LangChainDocumentProcessor
from src.vectorstore.lc_chroma_store import LangChainChromaStore


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
    print("  CBSE Class 10 AI Tutor - Setup (LangChain)")
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
    print("  1. Load and process all PDFs from data/raw/ (using LangChain)")
    print("  2. Generate embeddings using sentence-transformers")
    print("  3. Create ChromaDB vector database")
    print("="*60)
    
    response = input("\nProceed with setup? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Setup cancelled.")
        sys.exit(0)
    
    print("\n" + "="*60)
    print("Starting setup process...")
    print("="*60)
    
    # Initialize LangChain components
    print("\n[1/3] Initializing components...")
    processor = LangChainDocumentProcessor(
        chunk_size=config['chunking']['chunk_size'],
        chunk_overlap=config['chunking']['chunk_overlap']
    )
    
    db = LangChainChromaStore(
        persist_directory=config['vectorstore']['persist_directory'],
        collection_name=config['vectorstore']['collection_name'],
        embedding_model=config['embedding']['model_name'],
        device=config['embedding']['device']
    )
    
    # Clear existing data
    if len(db.vectorstore.get()['ids']) > 0:
        print("⚠️  Existing database found. Clearing...")
        db.vectorstore.delete_collection()
        # Re-initialize to create fresh collection
        db = LangChainChromaStore(
            persist_directory=config['vectorstore']['persist_directory'],
            collection_name=config['vectorstore']['collection_name'],
            embedding_model=config['embedding']['model_name'],
            device=config['embedding']['device']
        )
    
    # Step 2: Load and Chunk PDFs
    print("\n[2/3] Processing PDFs (this may take a few minutes)...")
    chunks = processor.process_pdfs("data/raw")
    
    if not chunks:
        print("❌ No documents loaded. Please check your PDFs.")
        sys.exit(1)
    
    # Step 3: Add to Vector DB
    print("\n[3/3] Generating embeddings and adding to database...")
    db.vectorstore.add_documents(chunks)
    
    # Print final stats
    print("\n" + "="*60)
    print("✅ Setup Complete!")
    print("="*60)
    
    count = len(db.vectorstore.get()['ids'])
    print(f"\n📊 Database Statistics:")
    print(f"  • Collection: {db.collection_name}")
    print(f"  • Total chunks: {count}")
    print(f"  • Storage location: {db.persist_directory}")
    
    print("\n" + "="*60)
    print("🚀 You're ready to start learning!")
    print("Run: python main.py")
    print("="*60)


if __name__ == "__main__":
    main()
