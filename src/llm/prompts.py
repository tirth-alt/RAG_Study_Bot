"""
Prompt Templates Module
Defines prompts for the tutoring LLM.
"""


class TutorPrompts:
    """Prompts for the CBSE Class 10 AI Tutor."""
    
    # System prompt
    SYSTEM_PROMPT = """You are a helpful CBSE Class 10 tutor for English and Social Science.

CORE RULES:
1. Answer based on the CONTEXT provided below
2. If context has partial info, use it and say "Based on the textbook..."
3. If context has NO relevant info at all, say: "I don't find this in the textbook sections I can see."
4. Keep answers concise (2-5 sentences for most questions)
5. For lists (chapters, features, etc.), use bullet points
6. Use simple, Class 10-level language

IMPORTANT:
- If you see chapter titles/numbers in context, list them
- Don't make up specific details not in context
- It's okay to synthesize info from multiple context sources
- Be helpful and educational, not overly strict

Remember: Help the student learn from their textbook!"""

    @staticmethod
    def get_query_prompt(context: str, question: str, chat_history: str = "") -> str:
        """
        Generate the complete prompt for a query.
        
        Args:
            context: Retrieved textbook context
            question: Student's question
            chat_history: Previous conversation (optional)
            
        Returns:
            Complete prompt string
        """
        prompt = f"""{TutorPrompts.SYSTEM_PROMPT}

CONTEXT:
{context}
"""
        
        if chat_history:
            prompt += f"""
HISTORY:
{chat_history}
"""
        
        prompt += f"""
QUESTION: {question}

ANSWER:"""
        
        return prompt
    
    @staticmethod
    def get_welcome_message() -> str:
        """Get welcome message for students."""
        return """
╔══════════════════════════════════════════════════════════╗
║     🎓 CBSE Class 10 AI Tutor - English & Social Science     ║
╚══════════════════════════════════════════════════════════╝

Hello! I'm your friendly CBSE Class 10 tutor. I'm here to help you 
with English and Social Science based on your textbooks.

Ask me anything from your syllabus:
  📚 English: Literature, grammar, writing
  🌍 Social Science: History, geography, civics, economics

Tips for better answers:
  ✓ Be specific with your questions
  ✓ Mention the chapter if you remember
  ✓ Ask follow-up questions for clarification

Commands:
  /clear  - Start a new topic
  /help   - Show this message again
  /exit   - Quit the tutor

Let's start learning! What would you like to know?
"""

    @staticmethod
    def get_help_message() -> str:
        """Get help message."""
        return """
📖 How to use this tutor:
  
  1. Ask questions about your English or Social Science textbooks
  2. I'll provide answers based on the textbook content
  3. Ask follow-up questions to understand better
  
Commands:
  /clear  - Clear chat history and start fresh
  /help   - Show this help message
  /exit   - Exit the tutor
  
Example questions:
  - "What is democracy?"
  - "Explain the theme of Nelson Mandela chapter"
  - "What are the features of federalism?"
  - "Summarize the poem 'Dust of Snow'"
"""


if __name__ == "__main__":
    # Test prompts
    print(TutorPrompts.get_welcome_message())
    
    sample_context = "Democracy is a form of government in which people elect their representatives."
    sample_question = "What is democracy?"
    
    prompt = TutorPrompts.get_query_prompt(sample_context, sample_question)
    print(f"\n{'='*60}\nSample Prompt:\n{'='*60}")
    print(prompt)
