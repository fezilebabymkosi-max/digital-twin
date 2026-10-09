"""
tools/productivity.py
Provides utility functions for:
1. Economic & Career Enablement (Skill-to-Income mapping, Remote Work Parsing, Gig Prompts)
2. Task & Workflow Productivity (Note formatting, Action item extraction, Daily Briefings)
"""

import json
from datetime import datetime

class ProductivityTools:
    
    # ==========================================
    # 1. MONETIZATION & CAREER ENGINE
    # ==========================================
    
    @staticmethod
    def map_skills_to_income(user_skills: list[str]) -> list[dict]:
        """
        Maps technical skills to actionable online income avenues and remote gig opportunities.
        """
        income_routes = {
            "python": {
                "avenue": "Automation & Web Scraping Freelancing",
                "platforms": ["Upwork", "Fiverr", "Contra"],
                "offer": "Build custom lead generation scrapers or data processing scripts for SMBs."
            },
            "rag systems": {
                "avenue": "Custom AI Agent / Knowledge Base Development",
                "platforms": ["Upwork", "Direct B2B Outreach"],
                "offer": "Build custom Chat-with-your-Docs tools for local businesses using ChromaDB & Gemini."
            },
            "llm pipelines": {
                "avenue": "Prompt Engineering & Workflow Automation",
                "platforms": ["Zapier/Make Consulting", "Upwork"],
                "offer": "Connect Google Gemini to CRM/Email workflows for automated customer support."
            },
            "automation": {
                "avenue": "API & Script Integration Services",
                "platforms": ["Fiverr", "Github Services"],
                "offer": "Write Python automation scripts to streamline manual computer tasks."
            }
        }
        
        matched_avenues = []
        for skill in user_skills:
            key = skill.lower().strip()
            if key in income_routes:
                matched_avenues.append(income_routes[key])
                
        # Default fallback if skills are custom or unmapped
        if not matched_avenues:
            matched_avenues.append({
                "avenue": "Technical Writing & Micro-Tasking",
                "platforms": ["Medium Partner Program", "RemoteOK", "We Work Remotely"],
                "offer": "Document your Digital Twin build process as technical tutorials."
            })
            
        return matched_avenues

    @staticmethod
    def format_proposal_template(job_title: str, client_problem: str, relevant_skills: list[str]) -> str:
        """
        Generates a high-converting, direct freelancing pitch template for job applications.
        """
        skills_formatted = ", ".join(relevant_skills)
        return f"""
### Freelance Pitch Proposal: {job_title}

**Opening:**
"Hi there, I saw your listing regarding {client_problem}. I specialize in {skills_formatted} and can solve this efficiently."

**Proposed Solution:**
1. Analyze requirements and set up a lightweight local pipeline.
2. Build and test the Python automation/LLM script within 48 hours.
3. Deliver documented code with setup instructions.

**Call to Action:**
"Let's jump on a quick 5-minute chat to discuss the specifics. I can start immediately."
""".strip()

    # ==========================================
    # 2. PERSONAL PRODUCTIVITY & TASK ENGINE
    # ==========================================

    @staticmethod
    def extract_action_items(notes_text: str) -> list[dict]:
        """Parses raw unstructured text to find explicit tasks and to-dos."""
        lines = [line.strip() for line in notes_text.split("\n") if line.strip()]
        tasks = []
        
        for idx, line in enumerate(lines):
            if line.startswith("- [ ]") or line.lower().startswith("todo:") or "action:" in line.lower():
                task_content = line.replace("- [ ]", "").replace("TODO:", "").replace("todo:", "").replace("action:", "").strip()
                tasks.append({
                    "task_id": f"task_{idx+1}",
                    "description": task_content,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "status": "pending"
                })
        return tasks

    @staticmethod
    def format_daily_briefing(user_name: str, tasks: list[dict], income_routes: list[dict], retrieved_context: list[str]) -> str:
        """Assembles a structured Markdown executive dashboard for daily focus & income execution."""
        date_str = datetime.now().strftime("%A, %B %d, %Y")
        
        briefing = [
            f"# 🚀 Executive Daily Briefing for {user_name}",
            f"**Date:** {date_str}\n",
            "## 💰 Income Opportunities & Skill Monetization"
        ]
        
        if income_routes:
            for route in income_routes:
                briefing.append(f"- **{route['avenue']}** (`{', '.join(route['platforms'])}`)")
                briefing.append(f"  *Offer:* {route['offer']}")
        else:
            briefing.append("- No active income routes mapped.")

        briefing.append("\n## 📌 Action Items & Tasks")
        if tasks:
            for t in tasks:
                briefing.append(f"- [ ] `{t['task_id']}` {t['description']}")
        else:
            briefing.append("- No pending action items parsed.")

        briefing.append("\n## 🧠 Digital Twin Memory Context")
        if retrieved_context:
            for ctx in retrieved_context:
                briefing.append(f"> {ctx}")
        else:
            briefing.append("> No relevant context retrieved.")

        return "\n".join(briefing)