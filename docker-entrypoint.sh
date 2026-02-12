#!/bin/bash
set -e

echo "🚀 Starting CBSE Tutor API..."

# Start Ollama in background
echo "📦 Starting Ollama..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama..."
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama ready!"
        break
    fi
    sleep 1
done

# Pull model if not exists
echo "🤖 Checking model..."
ollama pull llama3.2 || echo "Model already exists"

# Start the API
echo "🎓 Starting API server..."
exec uvicorn api:app --host 0.0.0.0 --port 8000
