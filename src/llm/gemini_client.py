"""
Gemini Client Module
Interface with Google Gemini API using the new google-genai package.
"""

import os
from typing import Optional
import google.genai as genai
from google.genai import types
from dotenv import load_dotenv


class GeminiClient:
    """Client for Google Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-flash", 
                 temperature: float = 0.7, max_tokens: int = 500):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Google API key (or load from .env)
            model_name: Gemini model to use
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
        """
        # Load API key
        if api_key is None:
            load_dotenv()
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key or api_key == "your_api_key_here":
            raise ValueError(
                "❌ Gemini API key not found!\n"
                "Please set GEMINI_API_KEY in .env file.\n"
                "Get your key from: https://makersuite.google.com/app/apikey"
            )
        
        # Configure Gemini with new API
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        print(f"✅ Gemini API initialized with model: {model_name}")
    
    def generate_response(self, prompt: str) -> str:
        """
        Generate response from Gemini.
        
        Args:
            prompt: Complete prompt string
            
        Returns:
            Generated response text
        """
        try:
            # Generate response using new API
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                )
            )
            
            # Extract text
            if response.text:
                return response.text.strip()
            else:
                return "I'm having trouble generating a response. Please try rephrasing your question."
            
        except Exception as e:
            # Return full error to debug
            return f"❌ Gemini Error: {str(e)}"
    
    def test_connection(self) -> bool:
        """
        Test if Gemini API is accessible.
        
        Returns:
            True if connected, False otherwise
        """
        try:
            # Try a simple generation to test connection
            response = self.client.models.generate_content(
                model=self.model_name,
                contents="Test"
            )
            return True
        except:
            return False


if __name__ == "__main__":
    # Test Gemini client
    try:
        client = GeminiClient()
        
        test_prompt = "Explain what democracy means in simple terms for a Class 10 student."
        print(f"\nTest Prompt: {test_prompt}")
        
        response = client.generate_response(test_prompt)
        print(f"\nResponse:\n{response}")
        
    except ValueError as e:
        print(str(e))
        print("\n💡 Create a .env file with your GEMINI_API_KEY to test this module.")
