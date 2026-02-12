"""
Ollama Client Module
Interface with locally running Ollama models.
"""

import requests
from typing import Optional


class OllamaClient:
    """Client for Ollama local LLM."""
    
    def __init__(self, model_name: str = "llama3.2", 
                 temperature: float = 0.8, max_tokens: int = 500,
                 base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama client.
        
        Args:
            model_name: Ollama model to use (e.g., llama3.2, mistral, phi)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
            base_url: Ollama server URL
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        
        # Test connection
        try:
            response = requests.get(f"{base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                print(f"✅ Ollama connected: {model_name}")
            else:
                raise ConnectionError("Ollama server not responding")
        except Exception as e:
            raise ValueError(
                f"❌ Cannot connect to Ollama!\n"
                f"Please install and start Ollama:\n"
                f"1. Install: https://ollama.ai/download\n"
                f"2. Run: ollama pull {model_name}\n"
                f"3. Ollama should auto-start\n"
                f"Error: {str(e)}"
            )
    
    def generate_response(self, prompt: str) -> str:
        """
        Generate response from Ollama.
        
        Args:
            prompt: Complete prompt string
            
        Returns:
            Generated response text
        """
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=60  # Give it time to generate
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                return f"❌ Ollama error: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            return "⚠️ Request timed out. The model might be too slow."
        except Exception as e:
            return f"❌ Error generating response: {str(e)}"
    
    def test_connection(self) -> bool:
        """
        Test if Ollama server is running and responding.
        
        Returns:
            True if connected, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False


if __name__ == "__main__":
    # Test Ollama client
    try:
        client = OllamaClient()
        
        test_prompt = "Explain democracy in one sentence."
        print(f"\nTest Prompt: {test_prompt}")
        
        response = client.generate_response(test_prompt)
        print(f"\nResponse:\n{response}")
        
    except ValueError as e:
        print(str(e))
