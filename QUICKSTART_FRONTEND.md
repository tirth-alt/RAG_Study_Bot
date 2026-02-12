# Quick Start - Frontend & API

## Run Everything

Open 2 terminals:

**Terminal 1:** Ollama (if not running)
```bash
ollama serve
```

**Terminal 2:** API + Frontend
```bash
cd /Users/apple/Documents/RAG_Project
source .venv/bin/activate
uvicorn api:app --reload
```

## Access

🌐 **Open in browser:** http://localhost:8000

That's it! The frontend will automatically load and connect to the API.

## Features

- ✨ Clean, modern chat interface
- 🎨 Gradient background and smooth animations
- 📱 Fully responsive (works on mobile)
- 💬 Real-time chat with typing indicators
- 📚 Source citations displayed with each answer
- 🔄 Clear chat history button
- 💡 Suggested questions to get started

## Troubleshooting

**"API not connected" error:**
- Make sure Ollama is running: `ollama serve`
- Check API is running on port 8000

**Blank screen:**
- Check browser console (F12) for errors
- Ensure `static/` folder exists with all 3 files

**Answers not showing:**
- Verify vectorstore has documents: http://localhost:8000/api/stats
- Check: http://localhost:8000/api/health
