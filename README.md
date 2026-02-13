# 🤖 AI-Powered RAG Tutor

An intelligent tutoring system for CBSE Class 10 Social Science using Retrieval-Augmented Generation (RAG). Ask questions and get accurate answers with source citations from the official NCERT textbooks.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🎯 **Accurate Answers**: Responses grounded in NCERT textbooks
- 📚 **Source Citations**: Every answer includes page references
- 💬 **Session-Based Memory**: Each user gets isolated conversation history
- 🔍 **Semantic Search**: ChromaDB vector database for intelligent retrieval
- 🌐 **REST API**: Easy integration with any frontend
- 🎨 **Modern UI**: Beautiful purple-themed chat interface

## 🏗️ Architecture

```
RAG Pipeline:
User Question → Query Reformulation → Vector Search → Context Retrieval
              → LLM Generation → Answer + Sources
```

**Tech Stack:**
- **Backend**: FastAPI, Python 3.9+
- **LLM**: Ollama (local) / Google Gemini (cloud)
- **Vector DB**: ChromaDB with sentence-transformers
- **Embeddings**: all-MiniLM-L6-v2
- **Frontend**: Vanilla HTML/CSS/JavaScript

## 📊 Data

- **1,434 document chunks** from NCERT Class 10 Social Science
- Subjects: Political Science, History, Geography, Economics
- Metadata: subject, source file, page numbers

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Ollama (for local development)
- 4GB+ RAM

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/rag-tutor.git
cd rag-tutor
```

2. **Install dependencies**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. **Set up Ollama** (local development)
```bash
# Install from https://ollama.ai
ollama pull llama3.2
ollama serve  # Keep running in separate terminal
```

4. **Initialize the database**
```bash
python setup.py
```

5. **Start the API server**
```bash
uvicorn api:app --reload --port 8000
```

6. **Access the app**
- Frontend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🌐 Production Deployment

### Railway (Recommended)

1. **Get Gemini API Key** (free): https://aistudio.google.com/app/apikey

2. **Deploy to Railway**:
   - Fork this repo
   - Connect to Railway: https://railway.app
   - Add environment variable: `GEMINI_API_KEY=your_key`
   - Deploy with `config.prod.yaml` (uses Gemini)

3. **Your live URL**: `https://your-app.railway.app`

See [deployment details](#deployment-options) below for other platforms.

## 📖 Usage

### Web Interface

1. Open http://localhost:8000
2. Ask questions like:
   - "What is democracy?"
   - "Explain nationalism"
   - "What are the features of federalism?"
3. Get answers with source citations

### API

**Chat Endpoint:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is democracy?"}'
```

**Response:**
```json
{
  "answer": "Democracy is a form of government...",
  "sources": [
    {"subject": "Polity", "filename": "Polity", "page": 7}
  ],
  "session_id": "abc-123",
  "success": true
}
```

**Other Endpoints:**
- `GET /api/health` - Health check
- `GET /api/stats` - Database statistics
- `POST /api/clear?session_id=xyz` - Clear session history

## ⚙️ Configuration

### Local Development (Ollama)
Uses `config/config.local.yaml`:
```yaml
llm:
  provider: "ollama"
  model: "llama3.2"
  temperature: 0.5
```

### Production (Gemini)
Uses `config/config.prod.yaml`:
```yaml
llm:
  provider: "gemini"
  model: "models/gemini-1.5-flash"
  temperature: 0.7
```

### Environment Variables
Create `.env` file:
```bash
GEMINI_API_KEY=your_api_key_here  # For production only
```

## 🧪 Testing

```bash
# Test retrieval
python -m pytest tests/

# Test API manually
python test_api.py
```

## 📁 Project Structure

```
rag-tutor/
├── api.py                 # FastAPI application
├── main.py                # CLI interface & CBSETutor class
├── setup.py               # Database initialization
├── config/
│   ├── config.yaml        # Active config (copied from local/prod)
│   ├── config.local.yaml  # Ollama config
│   └── config.prod.yaml   # Gemini config
├── src/
│   ├── chat/              # Memory & session management
│   ├── ingestion/         # PDF processing & chunking
│   ├── llm/               # LLM clients (Ollama/Gemini)
│   ├── retrieval/         # Vector search & retrieval
│   └── vectorstore/       # ChromaDB interface
├── static/                # Frontend files
│   ├── index.html
│   ├── style.css
│   └── script.js
├── data/                  # NCERT PDF textbooks
└── vectorstore/           # ChromaDB database
```

## 🔧 Advanced Configuration

### Retrieval Settings
```yaml
retrieval:
  top_k: 7                 # Number of chunks to retrieve
  score_threshold: 0.5     # Minimum similarity score
```

### LLM Settings
```yaml
llm:
  temperature: 0.7         # Creativity (0-1)
  max_tokens: 500          # Response length
```

### Chunking Settings
```yaml
chunking:
  chunk_size: 1200         # Characters per chunk
  chunk_overlap: 350       # Overlap between chunks
```

## 🐳 Docker Deployment

```bash
# Build
docker build -t rag-tutor .

# Run
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  rag-tutor
```

## 📊 Performance

- **Response Time**: ~2-3s (includes retrieval + generation)
- **Database Size**: 1,434 chunks (~2.5MB embeddings)
- **Memory Usage**: ~500MB (with model loaded)
- **Concurrent Users**: Supports multiple sessions

## 🛠️ Development

### Adding New Textbooks

1. Place PDFs in `data/`
2. Run `python setup.py` to re-index
3. Restart the API

### Modifying Prompts

Edit `src/llm/prompts.py`:
```python
class TutorPrompts:
    @staticmethod
    def get_query_prompt(context, question, history):
        # Customize prompt here
```

## 🐛 Troubleshooting

**Ollama not connecting?**
```bash
# Check if running
curl http://localhost:11434/api/tags

# Restart Ollama
killall ollama
ollama serve
```

**ChromaDB issues?**
```bash
# Rebuild database
rm -rf vectorstore/
python setup.py
```

**Port 8000 in use?**
```bash
# Free the port
lsof -ti:8000 | xargs kill -9
```

## 🎯 Deployment Options

### 1. Railway.app (Easiest)
- Free $5 credit
- Auto-deploys from GitHub
- Built-in SSL
- Cost: ~$5-10/month

### 2. Render.com
- Free tier available
- Docker support
- Auto SSL
- Cost: Free or $7/month

### 3. DigitalOcean/AWS/GCP
- Full control
- Requires manual setup
- Cost: $12-50/month

---

**Built with ❤️ using RAG + Vector Search + LLMs**

⭐ Star this repo if you find it helpful!
