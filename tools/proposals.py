"""
tools/proposals.py
Engine for formatting structured proposal prompts for client pitches.
"""

class ProposalEngine:
    def format_proposal_prompt(self, job_description: str) -> str:
        """Formats a job description into a targeted pitch generation prompt."""
        return f"""
You are acting as Fezile Brian Mkosi's Digital Twin. 
Draft a high-converting, professional client proposal based on the following job description.

### JOB REQUIREMENTS:
{job_description}

### INSTRUCTIONS:
- Directly address the client's needs.
- Cite relevant live projects (e.g., oasis.org.za, cipa.org.za) and Salesforce/WordPress experience where relevant.
- Keep the tone professional, confident, and direct.
- Include a clear call to action proposing a kickoff call.
"""