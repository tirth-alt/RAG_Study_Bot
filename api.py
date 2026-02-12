"""
FastAPI REST API for CBSE Class 10 AI Tutor
Provides HTTP endpoints for RAG-based tutoring system.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import yaml
from main import CBSETutor
from src.chat.session_manager import SessionManager

# Initialize FastAPI app
app = FastAPI(
    title="CBSE Class 10 AI Tutor API",
    description="RAG-based tutoring system for CBSE Class 10 Social Science",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
tutor = None
session_manager = None


# Request/Response models
class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None  # Session tracking
    clear_history: bool = False


class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]  # Accept any type for values
    session_id: str  # Return session ID to client
    success: bool = True


class HealthResponse(BaseModel):
    status: str
    ollama_connected: bool
    database_size: int


class StatsResponse(BaseModel):
    collection_name: str
    document_count: int
    subjects: Dict[str, int]


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize the tutor on startup."""
    global tutor, session_manager
    print("🔄 Initializing CBSE Class 10 AI Tutor API...")
    tutor = CBSETutor()
    session_manager = SessionManager(session_timeout_minutes=60)
    print("✅ API ready!")


# Health check endpoint
@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Check if the API and dependencies are running."""
    if tutor is None:
        raise HTTPException(status_code=503, detail="Tutor not initialized")
    
    try:
        # Test Ollama connection
        ollama_status = tutor.llm.test_connection()
        db_size = tutor.retriever.chroma_db.collection.count()
        
        return HealthResponse(
            status="healthy",
            ollama_connected=ollama_status,
            database_size=db_size
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")


# Main chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a student's question and return an answer.
    
    Args:
        request: ChatRequest with question and optional clear_history flag
        
    Returns:
        ChatResponse with answer and sources
    """
    if tutor is None or session_manager is None:
        raise HTTPException(status_code=503, detail="Tutor not initialized")
    
    try:
        # Get or create session-specific memory
        session_id, memory = session_manager.get_memory(request.session_id)
        
        # Clear history if requested
        if request.clear_history:
            memory.clear()
        
        # Get chat history for query reformulation
        history_exchanges = memory.get_history()
        
        # Get relevant context with reformulation
        context, sources = tutor.retriever.get_context_string(
            request.question,
            chat_history=history_exchanges
        )
        
        # Get conversation history for prompt
        history = memory.get_history_string(num_exchanges=2)
        
        # Build prompt
        from src.llm.prompts import TutorPrompts
        prompt = TutorPrompts.get_query_prompt(context, request.question, history)
        
        # Generate response
        response = tutor.llm.generate_response(prompt)
        
        # Save to session memory
        memory.add_exchange(request.question, response)
        
        # Format sources
        formatted_sources = []
        for source in sources:
            formatted_sources.append({
                "subject": source.get("subject", "Unknown"),
                "filename": source.get("source", "Unknown"),
                "page": source.get("page", 0)
            })
        
        return ChatResponse(
            answer=response,
            sources=formatted_sources,
            session_id=session_id,  # Return session ID
            success=True
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


# Clear chat history endpoint
@app.post("/api/clear")
async def clear_history(session_id: Optional[str] = None):
    """Clear chat history for a session."""
    if session_manager is None:
        raise HTTPException(status_code=503, detail="Session manager not initialized")
    
    try:
        if session_id:
            session_manager.clear_session(session_id)
        return {"message": "Chat history cleared", "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing history: {str(e)}")


# Database statistics endpoint
@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """Get database statistics."""
    if tutor is None:
        raise HTTPException(status_code=503, detail="Tutor not initialized")
    
    try:
        stats = tutor.retriever.chroma_db.get_stats()
        
        # Count documents by subject
        results = tutor.retriever.chroma_db.collection.get()
        subject_counts = {}
        for metadata in results.get('metadatas', []):
            subject = metadata.get('subject', 'Unknown')
            subject_counts[subject] = subject_counts.get(subject, 0) + 1
        
        return StatsResponse(
            collection_name=stats['collection_name'],
            document_count=stats['document_count'],
            subjects=subject_counts
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Root endpoint - serve frontend
@app.get("/")
async def root():
    """Serve the chat interface."""
    return FileResponse('static/index.html')


# API info  
@app.get("/api")
async def api_info():
    """API information."""
    return {
        "name": "CBSE Class 10 AI Tutor API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/api/health",
            "chat": "/api/chat (POST)",
            "clear": "/api/clear (POST)",
            "stats": "/api/stats"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
