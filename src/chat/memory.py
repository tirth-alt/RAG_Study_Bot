"""
Conversation Memory Module
Manages chat history for context preservation.
"""

from typing import List, Dict
from collections import deque


class ConversationMemory:
    """Manage conversation history."""
    
    def __init__(self, max_messages: int = 10):
        """
        Initialize conversation memory.
        
        Args:
            max_messages: Maximum number of messages to keep (must be even)
        """
        # Ensure even number for Q&A pairs
        if max_messages % 2 != 0:
            max_messages += 1
        
        self.max_messages = max_messages
        self.messages = deque(maxlen=max_messages)
    
    def add_message(self, role: str, content: str):
        """
        Add a message to history.
        
        Args:
            role: "user" or "assistant"
            content: Message content
        """
        self.messages.append({
            "role": role,
            "content": content
        })
    
    def add_exchange(self, user_message: str, assistant_message: str):
        """
        Add a complete Q&A exchange.
        
        Args:
            user_message: User's question
            assistant_message: Assistant's response
        """
        self.add_message("user", user_message)
        self.add_message("assistant", assistant_message)
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get conversation history.
        
        Returns:
            List of message dictionaries
        """
        return list(self.messages)
    
    def get_history_string(self, num_exchanges: int = 3) -> str:
        """
        Get formatted history string for prompt.
        
        Args:
            num_exchanges: Number of recent Q&A exchanges to include
            
        Returns:
            Formatted history string
        """
        if not self.messages:
            return ""
        
        # Get recent messages (each exchange is 2 messages)
        num_messages = min(num_exchanges * 2, len(self.messages))
        recent_messages = list(self.messages)[-num_messages:]
        
        # Format as conversation
        history_parts = []
        for msg in recent_messages:
            if msg["role"] == "user":
                history_parts.append(f"Student: {msg['content']}")
            else:
                history_parts.append(f"Tutor: {msg['content']}")
        
        return "\n".join(history_parts)
    
    def clear(self):
        """Clear conversation history."""
        self.messages.clear()
        print("💭 Chat history cleared. Starting fresh!")
    
    def is_empty(self) -> bool:
        """Check if memory is empty."""
        return len(self.messages) == 0
    
    def get_last_user_message(self) -> str:
        """
        Get the last user message.
        
        Returns:
            Last user message or empty string
        """
        for msg in reversed(self.messages):
            if msg["role"] == "user":
                return msg["content"]
        return ""


if __name__ == "__main__":
    # Test conversation memory
    memory = ConversationMemory(max_messages=6)
    
    # Add some exchanges
    memory.add_exchange("What is democracy?", "Democracy is a form of government...")
    memory.add_exchange("Give me an example", "India is an example of democracy...")
    memory.add_exchange("What about dictatorship?", "Dictatorship is different...")
    
    # Print history
    print("Conversation History:")
    print(memory.get_history_string())
    
    print(f"\nTotal messages: {len(memory.get_history())}")
    
    # Clear
    memory.clear()
    print(f"After clear: {len(memory.get_history())} messages")
