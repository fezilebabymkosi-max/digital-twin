"""
app.py
Main Orchestrator for your Digital Twin.
Combines Persona, ChromaDB RAG Memory, and Productivity/Monetization Tools powered by Google GenAI SDK.
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config.persona import get_system_instruction, USER_PROFILE
from memory.store import MemoryStore
from tools.productivity import ProductivityTools

# Load environment variables from .env
load_dotenv()

class DigitalTwin:
    def __init__(self):
        # 1. Initialize Gemini Client
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY missing from environment variables.")
        self.client = genai.Client(api_key=api_key)
        
        # 2. Initialize Vector Memory Store & Productivity Tools
        self.memory = MemoryStore()
        self.tools = ProductivityTools()
        
        # 3. Load Persona System Instructions
        self.system_instruction = get_system_instruction()

    def generate_response(self, user_prompt: str) -> str:
        """Retrieves memory context from ChromaDB and generates a persona-grounded response."""
        # Query ChromaDB memory for top 2 relevant context chunks
        retrieved_docs = self.memory.query_memory(user_prompt, n_results=2)
        context_str = "\n".join([f"- {doc}" for doc in retrieved_docs]) if retrieved_docs else "No specific memory found."

        # Construct augmented prompt with retrieved RAG context
        augmented_prompt = f"""
### RETRIEVED MEMORY CONTEXT
{context_str}

### USER INPUT
{user_prompt}
"""
# Call Gemini API with automatic model fallback for 503 high-demand errors
        try:
            response = self.client.models.generate_content(
                model="gemini-3.8-flash",
                contents=augmented_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.3
                )
            )
        except Exception as e:
            print(f"\n[Notice: gemini-3.8-flash busy, switching to fallback model...]")
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=augmented_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.3
                )
            )
        return response.text
    def run_daily_dashboard(self, raw_notes: str = "") -> str:
        """Executes a full daily executive briefing with skill monetization and action items."""
        # Map user skills to target income routes
        income_routes = self.tools.map_skills_to_income(USER_PROFILE["skills"])
        
        # Parse tasks from provided raw notes
        tasks = self.tools.extract_action_items(raw_notes) if raw_notes else []
        
        # Retrieve general memory background from ChromaDB
        retrieved_context = self.memory.query_memory("skills background experience", n_results=2)
        
        # Format briefing into structured Markdown
        return self.tools.format_daily_briefing(
            user_name=USER_PROFILE["name"],
            tasks=tasks,
            income_routes=income_routes,
            retrieved_context=retrieved_context
        )


if __name__ == "__main__":
    twin = DigitalTwin()
    print("\n--- Digital Twin Initialized ---")
    
    # Updated test query reflecting full profile
    query = "How can I start making money online this week using my Salesforce Operations, WordPress web design, and AI automation skills?"
    print(f"\nUser Query: {query}\n")
    print("Digital Twin Response:")
    print(twin.generate_response(query))