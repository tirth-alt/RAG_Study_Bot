# 🤖 RAG Study Bot: CBSE Class 10 AI Tutor

A high-performance RAG (Retrieval-Augmented Generation) application designed to help CBSE Class 10 students with Social Science.

**🚀 Live Demo:** [rag-study-bot-1.onrender.com](https://rag-study-bot-1.onrender.com)

## ✨ Features
- **Intelligent RAG**: Powered by LangChain 0.3 for accurate document retrieval.
- **Ultra-Fast Inference**: Uses Groq (Llama 3.3 70B) for sub-2s responses in production.
- **Local-First Vector DB**: Pre-computed ChromaDB vector store for instant searches.
- **Session Memory**: Context-aware conversations for follow-up questions.
- **Responsive UI**: Modern, glassmorphic chat interface.

## 🛠️ Tech Stack
- **Framework**: LangChain 0.3
- **Backend**: FastAPI (Python 3.10)
- **LLM**: Groq (Production) & Ollama (Local)
- **Vector DB**: ChromaDB
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **Frontend**: Vanilla HTML/CSS/JS

## 🚀 Quick Start (Local)

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Vector Store**:
   Add PDFs to `data/raw/` and run:
   ```bash
   python setup.py
   ```

3. **Run Application**:
   ```bash
   python main.py
   ```

## ☁️ Deployment
Deployed on **Render** using a size-optimized Docker image (~1.5GB) with CPU-only Torch.

---
Built with ❤️ for advanced AI tutoring.
