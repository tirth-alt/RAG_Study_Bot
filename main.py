"""
Main Application
CBSE Class 10 AI Tutor - RAG-based chatbot.
"""

import os
import sys
import yaml
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.vectorstore.embeddings import EmbeddingGenerator
from src.vectorstore.chroma_db import ChromaDBManager
from src.retrieval.retriever import Retriever
from src.llm.gemini_client import GeminiClient
from src.llm.ollama_client import OllamaClient
from src.llm.prompts import TutorPrompts
from src.chat.memory import ConversationMemory
from src.chat.interface import ChatInterface


class CBSETutor:
    """Main CBSE Tutor application."""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize the tutor application.
        
        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize components
        print("🔄 Initializing CBSE Class 10 AI Tutor...")
        
        # 1. Embedding generator
        self.embedder = EmbeddingGenerator(
            model_name=self.config['embedding']['model_name'],
            device=self.config['embedding']['device']
        )
        
        # 2. Vector database
        self.db = ChromaDBManager(
            persist_directory=self.config['vectorstore']['persist_directory'],
            collection_name=self.config['vectorstore']['collection_name']
        )
        
        # Check if database is populated
        if self.db.get_stats()["document_count"] == 0:
            print("\n❌ Vector database is empty!")
            print("Please run setup first: python setup.py")
            sys.exit(1)
        
        # 3. Retriever
        self.retriever = Retriever(
            embedding_generator=self.embedder,
            chroma_db=self.db,
            top_k=self.config['retrieval']['top_k']
        )
        
        # 4. LLM client (Ollama or Gemini)
        try:
            provider = self.config['llm']['provider'].lower()
            
            if provider == "ollama":
                self.llm = OllamaClient(
                    model_name=self.config['llm']['model'],
                    temperature=self.config['llm']['temperature'],
                    max_tokens=self.config['llm']['max_tokens']
                )
            else:  # gemini
                self.llm = GeminiClient(
                    model_name=self.config['llm']['model'],
                    temperature=self.config['llm']['temperature'],
                    max_tokens=self.config['llm']['max_tokens']
                )
        except ValueError as e:
            print(f"\n{str(e)}")
            sys.exit(1)
        
        # 5. Chat components
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
        Process a user query.
        
        Args:
            question: User's question
            
        Returns:
            Tuple of (response, sources)
        """
        # Get chat history for query reformulation
        history_exchanges = self.memory.get_history()
        
        # Get relevant context with reformulation
        context, sources = self.retriever.get_context_string(
            question,
            chat_history=history_exchanges
        )
        
        # Get conversation history
        history = self.memory.get_history_string(num_exchanges=2)
        
        # Build prompt
        prompt = TutorPrompts.get_query_prompt(context, question, history)
        
        # Generate response
        response = self.llm.generate_response(prompt)
        
        return response, sources
    
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
                
                # Get response
                response, sources = self.process_query(user_input)
                
                # Display response
                self.interface.display_response(response, sources)
                
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
