# CBSE Class 10 AI Tutor

A RAG-based (Retrieval-Augmented Generation) AI tutor for CBSE Class 10 students studying English and Social Science. The tutor provides answers based on CBSE textbooks and maintains conversation context.

## 🎯 Features

- **Textbook-based answers**: All responses are grounded in CBSE Class 10 textbooks
- **Conversational memory**: Maintains context across multiple questions
- **Source citations**: Shows which textbook pages answers come from
- **Free & open-source**: Uses free embedding models and LLMs
- **Simple terminal interface**: Easy to use chat interface

## 🏗️ Architecture

```
Student Question → Embedding → ChromaDB Search → Context Retrieval
                                                        ↓
Student ← Response ← Gemini LLM ← Context + Prompt
```

### Components

1. **PDF Ingestion**: Loads textbooks and splits into chunks
2. **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` model
3. **Vector Store**: ChromaDB for semantic search
4. **Retrieval**: Finds relevant textbook sections
5. **LLM**: Google Gemini API for generating responses
6. **Chat Interface**: Terminal-based conversation UI

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free tier available)
- CBSE Class 10 textbooks in PDF format

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Environment

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

### 3. Add Textbooks

Place your CBSE Class 10 PDF textbooks in the `data/raw/` directory:

```
data/raw/
├── english.pdf
└── social_science.pdf
```

### 4. Run Setup

Process the PDFs and create the vector database:

```bash
python setup.py
```

This will:
- Load all PDFs from `data/raw/`
- Split them into chunks
- Generate embeddings
- Create ChromaDB vector database

**Note**: First run will download the embedding model (~80MB).

### 5. Start Chatting!

```bash
python main.py
```

## 💬 Usage

### Commands

- `/help` - Show help message
- `/clear` - Clear chat history and start new topic
- `/exit` - Quit the tutor

### Example Questions

```
📝 You: What is democracy?

🎓 Tutor: Democracy is a form of government in which the people have 
the power to choose their representatives...

📚 Sources:
  [1] Social Science - Democratic Politics (Page 5)
```

## 📁 Project Structure

```
RAG_Project/
├── data/
│   ├── raw/                    # Place PDF textbooks here
│   └── processed/              # Processed data (auto-generated)
├── src/
│   ├── ingestion/              # PDF loading and chunking
│   ├── vectorstore/            # Embeddings and ChromaDB
│   ├── retrieval/              # Context retrieval
│   ├── llm/                    # Gemini API integration
│   └── chat/                   # Chat interface and memory
├── config/
│   └── config.yaml             # Configuration settings
├── vectorstore/                # ChromaDB storage (auto-generated)
├── setup.py                    # One-time setup script
└── main.py                     # Main application
```

## ⚙️ Configuration

Edit `config/config.yaml` to customize:

- **Chunk size**: Text chunk size for embeddings
- **Top-k retrieval**: Number of context chunks to retrieve
- **LLM temperature**: Response randomness (0-1)
- **Memory size**: Number of messages to remember

## 🔧 Troubleshooting

### "Vector database is empty"
Run `python setup.py` first to process your PDFs.

### "API key not found"
Make sure your `.env` file exists and contains a valid `GEMINI_API_KEY`.

### "No PDF files found"
Place your textbook PDFs in `data/raw/` directory.

### API quota exceeded
Gemini free tier has limits. Wait a bit or upgrade to paid tier.

## 🛣️ Roadmap

- [ ] Web UI with Streamlit
- [ ] Quiz generation feature
- [ ] Progress tracking
- [ ] Support for more subjects
- [ ] Mobile app

## 📝 License

This project is open-source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📧 Support

For questions or issues, please open a GitHub issue.

---

**Happy Learning! 📚**
