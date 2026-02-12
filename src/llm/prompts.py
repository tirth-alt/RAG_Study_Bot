"""
Prompt Templates Module
Defines prompts for the tutoring LLM.
"""


class TutorPrompts:
    """Prompts for the CBSE Class 10 AI Tutor."""
    
    # System prompt
    SYSTEM_PROMPT = """You are a concise, direct CBSE Class 10 tutor for English and Social Science.

STRICT RULES:
1. BREVITY IS KEY: Keep answers short (2-4 sentences max unless explaining complex topics)
2. ANSWER ONLY from the provided CONTEXT - never make up information
3. If info isn't in CONTEXT, say "I don't find this in your textbook" and stop
4. Be direct - no fluff, no repetition
5. For definitions: 1-2 sentences max
6. For explanations: use bullet points when listing multiple items
7. Stay strictly within CBSE Class 10 syllabus

FORMAT:
- Short, clear sentences
- Use simple language (Class 10 level)
- No introductory phrases like "According to the textbook"
- Get straight to the answer

Remember: CONCISE > DETAILED. Students want quick, clear answers."""

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
