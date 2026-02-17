"""
LangChain LLM Integration.
Wraps Ollama, Gemini, and Groq with LangChain's chat models.
"""

from typing import Optional
from langchain_community.chat_models import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os


class LangChainLLM:
    """
    Unified LLM interface using LangChain.
    Supports both Ollama (local) and Gemini (cloud).
    """
    
    def __init__(
        self,
        provider: str = "ollama",
        model: str = "llama3.2",
        temperature: float = 0.7,
        max_tokens: int = 500
    ):
        """
        Initialize LangChain LLM.
        
        Args:
            provider: 'ollama', 'gemini', or 'groq'
            model: Model name
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
        """
        self.provider = provider
        self.model_name = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Initialize the appropriate LLM
        if provider == "ollama":
            self._init_ollama()
        elif provider == "gemini":
            self._init_gemini()
        elif provider == "groq":
            self._init_groq()
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'ollama', 'gemini', or 'groq'.")
    
    def _init_ollama(self):
        """Initialize Ollama chat model."""
        print(f"🔄 Initializing Ollama with model: {self.model_name}...")
        
        self.llm = ChatOllama(
            model=self.model_name,
            temperature=self.temperature,
            num_predict=self.max_tokens
        )
        
        print(f"✅ Ollama initialized: {self.model_name} (connection will be tested on first use)")
    
    def _init_gemini(self):
        """Initialize Gemini chat model."""
        print(f"🔄 Initializing Gemini with model: {self.model_name}...")
        
        # Get API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "❌ GEMINI_API_KEY not found!\n"
                "Please set it in your .env file:\n"
                "GEMINI_API_KEY=your_api_key_here"
            )
        
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=api_key,
            temperature=self.temperature,
            max_output_tokens=self.max_tokens
        )
        
        print(f"✅ Gemini API initialized with model: {self.model_name}")
    
    def _init_groq(self):
        """Initialize Groq chat model."""
        print(f"🔄 Initializing Groq with model: {self.model_name}...")
        
        # Get API key
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "❌ GROQ_API_KEY not found!\n"
                "Please set it in your .env file:\n"
                "GROQ_API_KEY=your_groq_api_key_here\n"
                "Get a free key at: https://console.groq.com"
            )
        
        self.llm = ChatGroq(
            model=self.model_name,
            api_key=api_key,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        print(f"✅ Groq API initialized with model: {self.model_name}")
    
    def test_connection(self) -> bool:
        """Test if LLM is accessible."""
        try:
            response = self.llm.invoke([HumanMessage(content="test")])
            return True
        except:
            return False
    
    def generate(
        self,
        context: str,
        question: str,
        chat_history: Optional[list] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate a response using LangChain.
        
        Args:
            context: Retrieved context
            question: User question
            chat_history: List of (human, ai) message tuples
            system_prompt: Custom system prompt
            
        Returns:
            Generated response
        """
        # Build messages
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        
        # Add chat history
        if chat_history:
            for human_msg, ai_msg in chat_history:
                messages.append(HumanMessage(content=human_msg))
                messages.append(AIMessage(content=ai_msg))
        
        # Add current question with context
        user_message = f"""CONTEXT:
{context}

QUESTION: {question}

ANSWER (using ONLY the context above):"""
        
        messages.append(HumanMessage(content=user_message))
        
        # Generate response
        try:
            response = self.llm.invoke(messages)
            return response.content.strip()
        except Exception as e:
            error_msg = str(e)
            
            # Handle common errors
            if "quota" in error_msg.lower() or "resource" in error_msg.lower() or "rate" in error_msg.lower():
                return f"⚠️ API quota/rate limit error: {error_msg[:150]}"
            elif "api key" in error_msg.lower() or "401" in error_msg or "403" in error_msg:
                return f"❌ API key error. Please check your {self.provider.upper()} API key."
            else:
                return f"❌ LLM Error ({self.provider}): {error_msg[:200]}"
    
    def create_prompt_template(self) -> ChatPromptTemplate:
        """
        Create a LangChain prompt template for RAG.
        
        Returns:
            ChatPromptTemplate
        """
        template = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful CBSE Class 10 tutor for English and Social Science.

CRITICAL RULES:
1. Answer ONLY using the CONTEXT below - NO outside knowledge
2. Do NOT mix information from different geographic regions or time periods
3. Do NOT add examples not explicitly in the context
4. If context has specific examples (folk songs, customs), LIST THEM
5. Use bullet points for lists of specific items

Remember: ACCURACY and CONTEXT COHERENCE above all!"""),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", """CONTEXT:
{context}

QUESTION: {question}

ANSWER (using ONLY the context above):""")
        ])
        
        return template


# Backward compatibility
class OllamaClient:
    """Legacy Ollama client wrapper."""
    
    def __init__(self, model: str = "llama3.2", temperature: float = 0.5, max_tokens: int = 500):
        self.llm = LangChainLLM(
            provider="ollama",
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def generate_response(self, prompt: str) -> str:
        """Generate response from simple prompt."""
        messages = [HumanMessage(content=prompt)]
        try:
            response = self.llm.llm.invoke(messages)
            return response.content.strip()
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def test_connection(self) -> bool:
        """Test connection."""
        try:
            self.llm.llm.invoke([HumanMessage(content="Test")])
            return True
        except:
            return False


class GeminiClient:
    """Legacy Gemini client wrapper."""
    
    def __init__(self, model: str = "models/gemini-1.5-flash", temperature: float = 0.7, max_tokens: int = 500):
        self.llm = LangChainLLM(
            provider="gemini",
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def generate_response(self, prompt: str) -> str:
        """Generate response from simple prompt."""
        return self.llm.generate(context="", question=prompt)
    
    def test_connection(self) -> bool:
        """Test connection."""
        try:
            self.llm.llm.invoke([HumanMessage(content="Test")])
            return True
        except:
            return False


if __name__ == "__main__":
    # Test Ollama
    print("Testing Ollama...")
    llm = LangChainLLM(provider="ollama", model="llama3.2")
    
    context = "Democracy is a form of government where people elect their representatives."
    question = "What is democracy?"
    
    response = llm.generate(context=context, question=question)
    print(f"\nResponse: {response}")
