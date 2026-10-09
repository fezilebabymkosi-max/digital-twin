"""
app.py
Main Orchestrator for your Digital Twin.
Supports interactive mode switching (Client Pitch, Daily Planner, General Q&A).
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config.persona import get_system_instruction, USER_PROFILE
from memory.store import MemoryStore
from tools.productivity import ProductivityTools
from tools.proposals import ProposalEngine

load_dotenv()

class DigitalTwin:
    def __init__(self, mode: str = "default"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY missing from environment variables.")
        self.client = genai.Client(api_key=api_key)
        
        self.memory = MemoryStore()
        self.tools = ProductivityTools()
        self.proposal_engine = ProposalEngine()
        self.mode = mode
        self.system_instruction = get_system_instruction(mode)

    def set_mode(self, mode: str):
        """Switches operational mode dynamically."""
        self.mode = mode
        self.system_instruction = get_system_instruction(mode)
        print(f"\n[System] Digital Twin switched to '{mode}' mode.")

    def generate_response(self, user_prompt: str) -> str:
        """Retrieves memory context from ChromaDB and generates a response."""
        retrieved_docs = self.memory.query_memory(user_prompt, n_results=2)
        context_str = "\n".join([f"- {doc}" for doc in retrieved_docs]) if retrieved_docs else "No specific memory found."

        augmented_prompt = f"""
### RETRIEVED MEMORY CONTEXT
{context_str}

### USER INPUT
{user_prompt}
"""

        # Primary attempt with gemini-3.8-flash; fallback to gemini-flash-latest
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
            print(f"\n[Notice: Primary model unavailable ({type(e).__name__}), switching to fallback 'gemini-flash-latest'...]")
            try:
                response = self.client.models.generate_content(
                    model="gemini-flash-latest",
                    contents=augmented_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                        temperature=0.3
                    )
                )
            except Exception as fallback_err:
                return f"API Error: Both primary and fallback models are currently busy. Please try again in a few moments. ({fallback_err})"

        return response.text

    def draft_client_pitch(self, job_description: str) -> str:
        """Dedicated workflow for drafting client pitches."""
        self.set_mode("client_pitch")
        formatted_prompt = self.proposal_engine.format_proposal_prompt(job_description)
        return self.generate_response(formatted_prompt)

    def run_daily_planner(self, raw_notes: str) -> str:
        """Dedicated workflow for daily executive briefing."""
        self.set_mode("daily_planner")
        return self.run_daily_dashboard(raw_notes)

    def run_daily_dashboard(self, raw_notes: str = "") -> str:
        income_routes = self.tools.map_skills_to_income(USER_PROFILE["skills"])
        tasks = self.tools.extract_action_items(raw_notes) if raw_notes else []
        retrieved_context = self.memory.query_memory("skills background experience", n_results=2)
        
        return self.tools.format_daily_briefing(
            user_name=USER_PROFILE["name"],
            tasks=tasks,
            income_routes=income_routes,
            retrieved_context=retrieved_context
        )


if __name__ == "__main__":
    twin = DigitalTwin()
    print("\n==========================================")
    print("      DIGITAL TWIN INTERACTIVE CLI        ")
    print("==========================================")
    print("Commands:")
    print("  'pitch'   - Switch to Client Pitch Mode")
    print("  'plan'    - Switch to Daily Planner Mode")
    print("  'general' - Switch to General Mode")
    print("  'exit'    - Quit Application\n")

    while True:
        user_input = input("\nAsk Digital Twin > ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ["exit", "quit"]:
            print("Shutting down Digital Twin...")
            break
        elif user_input.lower() == "pitch":
            job_desc = input("\nPaste Client Job Description / Requirements:\n> ")
            print("\nGenerating Client Pitch...\n")
            print(twin.draft_client_pitch(job_desc))
        elif user_input.lower() == "plan":
            notes = input("\nPaste today's raw tasks/notes:\n> ")
            print("\nGenerating Daily Plan...\n")
            print(twin.run_daily_planner(notes))
        elif user_input.lower() == "general":
            twin.set_mode("default")
        else:
            print("\nDigital Twin Response:\n")
            print(twin.generate_response(user_input))