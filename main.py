"""
Main Application
CBSE Class 10 AI Tutor - RAG-based chatbot using LangChain.
"""

import os
import sys
import yaml
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# LangChain imports
from src.chain.rag_chain import CBSETutorRAG
from src.llm.prompts import TutorPrompts
from src.chat.memory import ConversationMemory
from src.chat.interface import ChatInterface


class CBSETutor:
    """Main CBSE Tutor application using LangChain."""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize the tutor application.
        
        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize LangChain RAG system
        print("🔄 Initializing CBSE Class 10 AI Tutor...")
        
        try:
            self.rag_tutor = CBSETutorRAG(config=self.config)
        except Exception as e:
            print(f"\n❌ Failed to initialize RAG system: {str(e)}")
            sys.exit(1)
        
        # Backward compatibility - expose components
        self.llm = self.rag_tutor.llm
        self.retriever = self.rag_tutor.retriever
        
        # Chat components
        self.memory = ConversationMemory(
            max_messages=self.config['chat']['memory_size']
        )
        
        self.interface = ChatInterface(
            show_sources=self.config['chat']['show_sources']
        )
        
        print("✅ All components initialized!\n")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        if not os.path.exists(config_path):
            print(f"❌ Configuration file not found: {config_path}")
            sys.exit(1)
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def process_query(self, question: str) -> tuple:
        """
        Process a user question using LangChain RAG.
        
        Args:
            question: User question
            
        Returns:
            Tuple of (answer, sources)
        """
        # Get chat history for context
        history = self.memory.get_history()
        
        # Use LangChain RAG to get answer
        result = self.rag_tutor.ask(
            question=question,
            chat_history=history
        )
        
        return result['answer'], result['sources']
    
    def run(self):
        """Run the chat interface."""
        # Display welcome message
        self.interface.display_welcome(TutorPrompts.get_welcome_message())
        
        # Main chat loop
        while True:
            # Get user input
            user_input = self.interface.get_user_input()
            
            # Skip empty input
            if not user_input:
                continue
            
            # Handle commands
            if self.interface.is_command(user_input):
                command = self.interface.handle_command(user_input)
                
                if command == "exit":
                    self.interface.display_goodbye()
                    break
                elif command == "clear":
                    self.memory.clear()
                    continue
                elif command == "help":
                    self.interface.display_help(TutorPrompts.get_help_message())
                    continue
            
            # Process question
            try:
                # Show thinking indicator
                self.interface.display_thinking()
                
                # Get response (sources are now dicts)
                response, sources = self.process_query(user_input)
                
                # Format sources for display (convert dicts to strings)
                formatted_sources = [
                    f"{s.get('subject', 'Unknown')} - {s.get('source', 'Unknown')} (Page {s.get('page', '?')})"
                    for s in sources
                ]
                
                # Display response
                self.interface.display_response(response, formatted_sources)
                
                # Add to memory
                self.memory.add_exchange(user_input, response)
                
            except Exception as e:
                self.interface.display_error(str(e))


def main():
    """Main entry point."""
    # Create and run tutor
    tutor = CBSETutor()
    tutor.run()


if __name__ == "__main__":
    main()
