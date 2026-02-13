# Quick Steps - Local Testing

## ✅ You Have: Gemini API Key

## Next: 3 Quick Steps

### Step 1: Add API Key to .env (1 min)

I just created a `.env` file. Now edit it:

```bash
# Open the file in your editor
code .env

# OR edit directly:
echo "GEMINI_API_KEY=YOUR_ACTUAL_KEY_HERE" > .env
```

Replace `YOUR_ACTUAL_KEY_HERE` with your actual key.

---

### Step 2: Switch to Gemini Config (30 sec)

```bash
cd /Users/apple/Documents/RAG_Project
cp config/config.prod.yaml config/config.yaml
```

This switches from Ollama to Gemini.

---

### Step 3: Test It! (2 min)

Stop your current API server (in the other terminal, press `Ctrl+C`), then:

```bash
cd /Users/apple/Documents/RAG_Project
source .venv/bin/activate
uvicorn api:app --reload --port 8000
```

**Test:** Go to http://localhost:8000 and ask a question!

✅ **Working?** → Ready for Railway!  
❌ **Error?** → Check the API key in `.env`

---

## After Testing Works

I'll help you:
- Push to GitHub
- Deploy to Railway  
- Get your live link!

**Try Step 1-3 now and let me know if Gemini works!** 🚀
