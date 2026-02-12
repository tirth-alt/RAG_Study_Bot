# Deployment Guide

## Quick Start - Run API Locally

```bash
# 1. Make sure Ollama is running
ollama serve

# 2. Start the API server (in new terminal)
cd /Users/apple/Documents/RAG_Project
source .venv/bin/activate
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

**API will be available at:** `http://localhost:8000`
**Interactive Docs:** `http://localhost:8000/docs`

---

## Testing the API

### Using curl
```bash
# Health check
curl http://localhost:8000/api/health

# Ask a question
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is democracy?"}'

# Get stats
curl http://localhost:8000/api/stats

# Clear history
curl -X POST http://localhost:8000/api/clear
```

### Using Python
```python
import requests

# Ask a question
response = requests.post('http://localhost:8000/api/chat', 
    json={'question': 'What is nationalism?'}
)
data = response.json()
print(data['answer'])
print(data['sources'])
```

---

## Frontend Integration Example

### React/Next.js
```javascript
// src/api/tutor.js
export async function askQuestion(question) {
  const response = await fetch('http://localhost:8000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });
  return response.json();
}

// In your component
const { answer, sources } = await askQuestion("What is federalism?");
```

### Example Frontend Component
```jsx
function ChatInterface() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  
  const handleSubmit = async () => {
    const response = await fetch('http://localhost:8000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });
    const data = await response.json();
    setAnswer(data.answer);
  };
  
  return (
    <div>
      <input value={question} onChange={e => setQuestion(e.target.value)} />
      <button onClick={handleSubmit}>Ask</button>
      <p>{answer}</p>
    </div>
  );
}
```

---

## Deployment Options

### Option 1: Local/LAN Access (Easiest)
**Good for:** Testing, home network
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```
Access from other devices: `http://YOUR_LOCAL_IP:8000`

### Option 2: Cloud VPS (Recommended)
**Good for:** Production, public access
**Platforms:** DigitalOcean ($24/mo), AWS EC2, Linode

**Steps:**
1. Get Ubuntu server (4GB+ RAM)
2. Install Python, Ollama, dependencies
3. Clone your project
4. Run setup.py to build database
5. Use systemd to run API as service
6. Set up Nginx reverse proxy
7. Add SSL with Let's Encrypt

### Option 3: Docker (Clean & Portable)
**Good for:** Reproducible deployments

Create `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Production Checklist

- [ ] Add API key authentication
- [ ] Set up rate limiting
- [ ] Configure CORS properly (specific origins, not "*")
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS
- [ ] Set up logging
- [ ] Monitor with health checks
- [ ] Backup vectorstore database

---

## Architecture

```
Frontend (React/Vue)
      ↓
   Internet
      ↓
  Nginx (SSL)
      ↓
FastAPI (api.py)
      ↓
RAG System (main.py)
      ↓
   ┌────────┬──────────┐
   ↓        ↓          ↓
ChromaDB  Ollama    Memory
```

---

## Next Steps

1. **Test API locally** - `uvicorn api:app --reload`
2. **Build simple frontend** - HTML/JS or React
3. **Choose deployment platform** - Local, VPS, or Docker
4. **Deploy backend** - API + Ollama + Database
5. **Deploy frontend** - Vercel, Netlify, or same server
6. **Connect them** - Update API URL in frontend

**Estimated time:** 2-4 hours for full deployment
