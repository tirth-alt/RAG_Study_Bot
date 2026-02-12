"""
Session Manager Module
Manages separate conversation sessions for multiple users.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional
from src.chat.memory import ConversationMemory


class SessionManager:
    """Manages conversation sessions for multiple users."""
    
    def __init__(self, session_timeout_minutes: int = 60):
        """
        Initialize session manager.
        
        Args:
            session_timeout_minutes: Minutes before inactive session expires
        """
        self.sessions: Dict[str, Dict] = {}
        self.timeout = timedelta(minutes=session_timeout_minutes)
    
    def create_session(self) -> str:
        """
        Create a new session.
        
        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'memory': ConversationMemory(),
            'created_at': datetime.now(),
            'last_accessed': datetime.now()
        }
        return session_id
    
    def get_memory(self, session_id: Optional[str] = None) -> tuple[str, ConversationMemory]:
        """
        Get or create memory for a session.
        
        Args:
            session_id: Optional session ID
            
        Returns:
            Tuple of (session_id, memory)
        """
        # Create new session if none provided or invalid
        if not session_id or session_id not in self.sessions:
            session_id = self.create_session()
        
        # Update last accessed time
        self.sessions[session_id]['last_accessed'] = datetime.now()
        
        # Clean up old sessions
        self._cleanup_old_sessions()
        
        return session_id, self.sessions[session_id]['memory']
    
    def clear_session(self, session_id: str):
        """Clear a session's memory."""
        if session_id in self.sessions:
            self.sessions[session_id]['memory'].clear()
    
    def delete_session(self, session_id: str):
        """Delete a session completely."""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def _cleanup_old_sessions(self):
        """Remove expired sessions."""
        now = datetime.now()
        expired = [
            sid for sid, data in self.sessions.items()
            if now - data['last_accessed'] > self.timeout
        ]
        for sid in expired:
            del self.sessions[sid]
    
    def get_stats(self) -> Dict:
        """Get session statistics."""
        return {
            'active_sessions': len(self.sessions),
            'sessions': [
                {
                    'id': sid[:8] + '...',
                    'messages': len(data['memory'].exchanges),
                    'age_minutes': (datetime.now() - data['created_at']).total_seconds() / 60
                }
                for sid, data in list(self.sessions.items())[:10]  # Show first 10
            ]
        }


if __name__ == "__main__":
    # Test session manager
    manager = SessionManager()
    
    # Create sessions
    sid1 = manager.create_session()
    sid2 = manager.create_session()
    
    print(f"Session 1: {sid1}")
    print(f"Session 2: {sid2}")
    
    # Get memories
    _, mem1 = manager.get_memory(sid1)
    _, mem2 = manager.get_memory(sid2)
    
    # Add different conversations
    mem1.add_exchange("What is democracy?", "Democracy is...")
    mem2.add_exchange("What is nationalism?", "Nationalism is...")
    
    print(f"\nSession 1 history: {len(mem1.exchanges)} exchanges")
    print(f"Session 2 history: {len(mem2.exchanges)} exchanges")
    
    print(f"\nStats: {manager.get_stats()}")
