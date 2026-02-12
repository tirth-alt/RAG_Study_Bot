"""
Terminal Chat Interface Module
Provides terminal-based chat UI.
"""

import sys
from typing import Optional
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class ChatInterface:
    """Terminal-based chat interface."""
    
    def __init__(self, show_sources: bool = True):
        """
        Initialize chat interface.
        
        Args:
            show_sources: Whether to display source information
        """
        self.show_sources = show_sources
        self.running = False
    
    def display_welcome(self, message: str):
        """Display welcome message."""
        print(Fore.CYAN + message)
    
    def display_help(self, message: str):
        """Display help message."""
        print(Fore.YELLOW + message)
    
    def get_user_input(self) -> str:
        """
        Get input from user.
        
        Returns:
            User input string
        """
        try:
            print(Fore.GREEN + "\n📝 You: " + Style.RESET_ALL, end="")
            user_input = input().strip()
            return user_input
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
    
    def display_thinking(self):
        """Display thinking indicator."""
        print(Fore.YELLOW + "🤔 Let me check your textbook..." + Style.RESET_ALL)
    
    def display_response(self, response: str, sources: Optional[list] = None):
        """
        Display assistant's response.
        
        Args:
            response: Response text
            sources: Optional list of source information
        """
        print(Fore.CYAN + "\n🎓 Tutor: " + Style.RESET_ALL + response)
        
        # Display sources if available and enabled
        if self.show_sources and sources:
            print(Fore.MAGENTA + "\n📚 Sources:")
            for i, source in enumerate(sources, 1):
                print(Fore.MAGENTA + f"  [{i}] {source}")
        
        print()  # Empty line for readability
    
    def display_error(self, error: str):
        """Display error message."""
        print(Fore.RED + f"\n❌ Error: {error}\n")
    
    def display_info(self, message: str):
        """Display info message."""
        print(Fore.YELLOW + f"\nℹ️  {message}\n")
    
    def handle_command(self, command: str) -> str:
        """
        Handle special commands.
        
        Args:
            command: Command string
            
        Returns:
            Command name or empty string
        """
        command = command.lower().strip()
        
        if command in ["/exit", "/quit", "/q"]:
            return "exit"
        elif command in ["/clear", "/new"]:
            return "clear"
        elif command in ["/help", "/h"]:
            return "help"
        
        return ""
    
    def is_command(self, text: str) -> bool:
        """Check if input is a command."""
        return text.startswith("/")
    
    def display_goodbye(self):
        """Display goodbye message."""
        message = """
╔══════════════════════════════════════════════════════════╗
║            👋 Thanks for studying with me!                   ║
║          Keep learning and asking questions! 📚              ║
╚══════════════════════════════════════════════════════════╝
"""
        print(Fore.CYAN + message)


if __name__ == "__main__":
    # Test the interface
    interface = ChatInterface()
    
    # Test welcome
    interface.display_welcome("Welcome to the tutor!")
    
    # Test response
    interface.display_response(
        "Democracy is a form of government where people elect their representatives.",
        sources=["Social Science - Democratic Politics (Page 5)"]
    )
    
    # Test command
    test_input = "/help"
    if interface.is_command(test_input):
        cmd = interface.handle_command(test_input)
        print(f"Command detected: {cmd}")
