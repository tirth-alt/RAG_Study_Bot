# 🚀 Quick Start Guide

## Step-by-Step Setup (15 minutes)

### 1️⃣ Get API Key (2 min)

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key

### 2️⃣ Configure Environment (1 min)

```bash
cd /Users/apple/Documents/RAG_Project

# Copy environment template
cp .env.example .env

# Edit and add your API key
nano .env
```

Replace `your_api_key_here` with your actual key:
```
GEMINI_API_KEY=AIzaSyC...your_actual_key_here
```

Save with: `Ctrl+O`, `Enter`, `Ctrl+X`

### 3️⃣ Add Textbooks (1 min)

Copy your CBSE PDF textbooks to `data/raw/`:

```bash
# Example:
cp ~/Downloads/english_class10.pdf data/raw/english.pdf
cp ~/Downloads/social_science_class10.pdf data/raw/social_science.pdf
```

### 4️⃣ Install Dependencies (3 min)

```bash
pip install -r requirements.txt
```

Wait for installation to complete...

### 5️⃣ Run Setup (5-10 min)

```bash
python setup.py
```

**What it does**:
- Processes your PDFs
- Creates embeddings
- Builds vector database

You'll see progress and final statistics.

### 6️⃣ Start Learning! (immediate)

```bash
python main.py
```

## 💬 Try These Questions

```
What is democracy?
Explain the Nelson Mandela chapter
What are features of federalism?
Tell me about the poem 'Dust of Snow'
```

## 🎮 Commands

- `/help` - Show help
- `/clear` - New topic (clear history)
- `/exit` - Quit

## ⚠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| "Vector database is empty" | Run `python setup.py` |
| "API key not found" | Check `.env` file |
| "No PDFs found" | Add PDFs to `data/raw/` |

## 📚 Learn More

- Full documentation: `README.md`
- Architecture details: See brain artifacts
- Configuration: `config/config.yaml`

---

**Need help? Check the README.md file!**
