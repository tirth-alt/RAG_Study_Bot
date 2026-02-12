# Ollama Setup Guide

## Quick Setup (5 minutes)

### Step 1: Install Ollama

**For macOS:**
```bash
# Download and install from website
open https://ollama.ai/download

# Or use Homebrew
brew install ollama
```

The installer will:
- Install Ollama
- Start the Ollama service automatically
- Add Ollama to your PATH

### Step 2: Download the Model

```bash
# Pull the llama3.2 model (about 2GB)
ollama pull llama3.2
```

This will download the model (one-time, takes 2-5 minutes).

### Step 3: Verify It's Running

```bash
# Check if Ollama is running
ollama list
```

You should see `llama3.2` in the list.

### Step 4: Run Your Tutor!

```bash
cd /Users/apple/Documents/RAG_Project
python main.py
```

## Advantages of Ollama

✅ **Completely Free** - No API costs
✅ **Offline** - Works without internet
✅ **Private** - All data stays on your machine
✅ **Fast** - Runs locally on your Mac
✅ **No Quotas** - Unlimited usage

## Alternative Models (Optional)

If llama3.2 is slow, try these smaller models:

```bash
# Faster but smaller
ollama pull phi3

# Medium speed/quality
ollama pull mistral
```

Then update `config/config.yaml`:
```yaml
llm:
  model: "phi3"  # or "mistral"
```

## Troubleshooting

**"Ollama not found"**
- Restart your terminal after installation
- Or manually start: `ollama serve`

**Model download slow**
- It's a one-time download
- You can use your tutor while it downloads other models

**Response too slow**
- Switch to a smaller model like `phi3`
- Or increase timeout in `ollama_client.py`

---

**Ready?** Follow the 3 steps above and you're set! 🚀
