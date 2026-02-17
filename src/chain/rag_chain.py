"""
LangChain RAG Chain.
Complete RAG pipeline using LangChain's ConversationalRetrievalChain.
"""

from typing import List, Dict, Tuple, Optional, Any
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

from src.vectorstore.lc_chroma_store import LangChainChromaStore
from src.llm.langchain_llm import LangChainLLM


class LangChainRAG:
    """
    Complete RAG system using LangChain.
    Combines retrieval, LLM, and conversation memory.
    """
    
    def __init__(
        self,
        llm_provider: str = "ollama",
        llm_model: str = "llama3.2",
        temperature: float = 0.7,
        top_k: int = 7,
        persist_directory: str = "./vectorstore",
        collection_name: str = "cbse_class10_textbooks"
    ):
        """
        Initialize RAG chain.
        
        Args:
            llm_provider: 'ollama' or 'gemini'
            llm_model: Model name
            temperature: LLM temperature
            top_k: Number of documents to retrieve
            persist_directory: Vector store directory
            collection_name: Chroma collection name
        """
        print("🔄 Initializing LangChain RAG system...")
        
        # Initialize vector store
        self.vectorstore = LangChainChromaStore(
            persist_directory=persist_directory,
            collection_name=collection_name
        )
        
        # Initialize LLM
        self.llm_client = LangChainLLM(
            provider=llm_provider,
            model=llm_model,
            temperature=temperature
        )
        
        # Get retriever
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": top_k}
        )
        
        # Create custom prompt
        self.prompt = self._create_prompt()
        
        print("✅ RAG system initialized!")
    
    def _create_prompt(self) -> ChatPromptTemplate:
        """Create prompt template."""
        system_template = """You are a helpful CBSE Class 10 tutor for English and Social Science.

CRITICAL RULES:
1. Answer ONLY using the CONTEXT below - NO outside knowledge
2. Do NOT mix information from different geographic regions or time periods
3. Do NOT add examples not explicitly in the context
4. If context has specific examples, LIST THEM
5. Use bullet points for lists

Remember: ACCURACY and CONTEXT COHERENCE above all!

CONTEXT:
{context}"""
        
        human_template = """{question}"""
        
        messages = [
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template(human_template)
        ]
        
        return ChatPromptTemplate.from_messages(messages)
    
    def ask(
        self,
        question: str,
        chat_history: Optional[List[Tuple[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Ask a question using the RAG chain.
        
        Args:
            question: User question
            chat_history: List of (human, ai) tuples
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        # Retrieve documents
        docs = self.retriever.invoke(question)
        
        # Extract context and sources
        context = "\n\n".join([doc.page_content for doc in docs])
        sources = [
            {
                "subject": doc.metadata.get("subject", "Unknown"),
                "filename": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", 0)
            }
            for doc in docs
        ]
        
        # Format chat history for LLM
        history_list = chat_history if chat_history else []
        
        # Generate answer
        answer = self.llm_client.generate(
            context=context,
            question=question,
            chat_history=history_list,
            system_prompt=self.prompt.messages[0].prompt.template
        )
        
        return {
            "answer": answer,
            "sources": sources,
            "source_documents": docs
        }
    
    def get_session_chain(self, session_id: str = "default"):
        """
        Get a conversational chain for a session.
        For backward compatibility.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Self (for chaining)
        """
        # LangChain RAG handles memory differently
        # We'll manage it at the API level with session manager
        return self


class CBSETutorRAG:
    """
    Main tutor interface using LangChain RAG.
    Drop-in replacement for the old CBSETutor class.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize tutor with optional config.
        
        Args:
            config: Configuration dictionary (optional)
        """
        if config is None:
            import yaml
            with open("config/config.yaml") as f:
                config = yaml.safe_load(f)
        
        llm_config = config.get("llm", {})
        retrieval_config = config.get("retrieval", {})
        vectorstore_config = config.get("vectorstore", {})
        
        self.rag = LangChainRAG(
            llm_provider=llm_config.get("provider", "ollama"),
            llm_model=llm_config.get("model", "llama3.2"),
            temperature=llm_config.get("temperature", 0.7),
            top_k=retrieval_config.get("top_k", 7),
            persist_directory=vectorstore_config.get("persist_directory", "./vectorstore"),
            collection_name=vectorstore_config.get("collection_name", "cbse_class10_textbooks")
        )
        
        self.llm = self.rag.llm_client  # For backward compatibility
        self.retriever = self.rag.retriever  # For backward compatibility
    
    def ask(self, question: str, chat_history: Optional[List[Tuple[str, str]]] = None) -> Dict[str, Any]:
        """
        Ask a question.
        
        Args:
            question: User question
            chat_history: Optional chat history
            
        Returns:
            Answer dictionary
        """
        return self.rag.ask(question, chat_history)


if __name__ == "__main__":
    # Test the RAG chain
    print("Testing LangChain RAG...")
    
    rag = LangChainRAG(
        llm_provider="ollama",
        llm_model="llama3.2"
    )
    
    result = rag.ask("What is democracy?")
    
    print(f"\n{'='*60}")
    print(f"Question: What is democracy?")
    print(f"{'='*60}")
    print(f"Answer: {result['answer']}")
    print(f"\nSources:")
    for i, source in enumerate(result['sources'], 1):
        print(f"  {i}. {source['subject']} - Page {source['page']}")
