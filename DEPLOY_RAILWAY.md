# 🎯 Quick Start: Railway Deployment

## What You're Getting
- 🌐 Live public URL for your resume
- 💰 Free to start ($5 credit), then ~$5-10/month
- ⚡ Fast Gemini API responses
- 🔒 Professional, secure hosting

---

## 5-Step Deployment (20 minutes)

### Step 1: Get Gemini API Key (2 min)
1. Visit: **https://aistudio.google.com/app/apikey**
2. Sign in with Google
3. Click "Create API Key"
4. **Copy the key** (starts with `AIza...`)

---

### Step 2: Test Locally with Gemini (5 min)

```bash
cd /Users/apple/Documents/RAG_Project

# Create .env file with your API key
echo "GEMINI_API_KEY=AIza_YOUR_ACTUAL_KEY_HERE" > .env

# Copy production config (uses Gemini)
cp config/config.prod.yaml config/config.yaml

# Stop current server (Ctrl+C in that terminal)
# Then restart with new config:
source .venv/bin/activate
uvicorn api:app --reload --port 8000
```

**Test:** Go to http://localhost:8000 and ask a question.  
✅ If it works → Gemini is ready!  
❌ If error → Check API key in `.env`

---

### Step 3: Push to GitHub (5 min)

```bash
# Make sure you're in project directory
cd /Users/apple/Documents/RAG_Project

# Initialize git (if needed)
git init
git add .
git commit -m "RAG Tutor ready for deployment"

# Create repo on GitHub:
# 1. Go to: https://github.com/new
# 2. Repository name: rag-tutor
# 3. Make it PUBLIC
# 4. DON'T check "Add README"
# 5. Click "Create repository"

# Push to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/rag-tutor.git
git branch -M main
git push -u origin main
```

---

### Step 4: Deploy on Railway (5 min)

1. **Sign up:** https://railway.app → "Login with GitHub"

2. **New Project:**
   - Click "New Project"
   - Choose "Deploy from GitHub repo"
   - Select `rag-tutor`
   - Railway starts building automatically!

3. **Add API Key:**
   - Click on your service (in Railway dashboard)
   - Go to "Variables" tab
   - Click "+ New Variable"
   - Name: `GEMINI_API_KEY`
   - Value: Your API key from Step 1
   - Click "Add"

4. **Get Your URL:**
   - Go to "Settings" tab  
   - Scroll to "Networking"
   - Click "Generate Domain"
   - **Copy the URL!** → `https://rag-tutor-production.up.railway.app`

---

### Step 5: Add to Resume (3 min)

**Example Resume Entry:**

```
PROJECTS
────────────────────────────────

🤖 AI-Powered RAG Tutor System
Intelligent tutoring chatbot using Retrieval-Augmented Generation (RAG)
to answer CBSE Class 10 Social Science questions with source citations

Tech Stack: Python • FastAPI • ChromaDB • Google Gemini • Vector Embeddings
• Processed 1,400+ document chunks with semantic search
• Session-based memory for isolated multi-user conversations
• REST API with auto-scaling cloud deployment

→ Live Demo: https://your-url.railway.app
→ GitHub: https://github.com/yourusername/rag-tutor
```

---

## 🎉 You're Done!

**Your tutor is now:**
- ✅ Live on the internet
- ✅ Accessible 24/7
- ✅ Ready for recruiters
- ✅ In your resume

**Test it:** Send the link to friends! 📱

---

## Troubleshooting

**"Build failed" on Railway?**
- Check all files are in GitHub
- Make sure `requirements.txt` is committed
- View build logs in Railway dashboard

**API errors when deployed?**
- Verify `GEMINI_API_KEY` is set in Railway Variables
- Check it doesn't have quotes around it
- Make sure Gemini API is enabled at Google AI Studio

**Want to update your app?**
```bash
git add .
git commit -m "Updated feature X"
git push
# Railway auto-deploys in ~2 minutes!
```

---

## Cost Breakdown

**Gemini API:** Free tier = 15 requests/min (plenty for portfolio)  
**Railway Hosting:**
- First month: FREE ($5 credit)
- After: ~$5-10/month

**Total: $5-10/month** ← Worth it for your career! 🚀

---

**Questions?** Railway docs: https://docs.railway.app
