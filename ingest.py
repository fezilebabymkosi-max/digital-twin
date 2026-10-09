"""
ingest.py
Ingests resume background, certifications, live web projects, and hands-on Salesforce portfolio projects into ChromaDB memory.
"""

from memory.store import MemoryStore

def load_user_credentials():
    store = MemoryStore()
    
    user_data = [
        """
        USER PROFILE: Fezile Brian Mkosi
        LOCATION: Cape Town, South Africa
        SUMMARY: Salesforce Operations Specialist, Web Developer, and AI Automation Engineer. Proven ability to clean lead data, structure CRM objects, build custom reports/dashboards, manage cases/knowledge bases, and execute full opportunity lifecycles in Salesforce alongside WordPress/Elementor/Divi web development.
        """,
        """
        LIVE WEB PORTFOLIO PROJECTS:
        - oasis.org.za: Live business site built using WordPress & Divi Builder. Responsive, custom styling, full web layout.
        - cipa.org.za: Live business site built using WordPress & Elementor. Clean structural navigation, mobile-optimized.
        """,
        """
        HANDS-ON SALESFORCE PORTFOLIO PROJECTS:
        1. Lead Management & Prospecting: Structured CSV lead data, imported records, created custom list views/filters ('Demo Leads'), associated leads with campaigns ('Social Media Conference Email Campaign'), and performed business case analyses.
        2. Opportunity Management & Deal Closing: Managed full deal lifecycles (FoodStars.org & Yaloo Search), configured Contact Roles, moved stages through Kanban, created Product catalogs, built Enterprise/Nonprofit Price Books, generated quote PDFs, emailed quotes, and created 12-month Contracts.
        3. Customer Success & Service Console: Created support cases (priority escalations), configured Data Categories ('Social Media Channel Management'), built/published 6 Knowledge Base articles, and streamlined agent resolution workflows.
        4. Reports & Dashboards: Developed Tabular, Summary, and Matrix reports, applied filters/groupings, generated report charts (Closed-Won by Industry, Working-Contacted by Lead Source), and built executive dashboards.
        """,
        """
        CERTIFICATIONS:
        - Google AI Professional Certificate (2026): AI Fundamentals, Prompt Engineering, Research & Data Analysis, Vibe Coding & Custom AI App Building.
        - Salesforce Sales Operations Professional Certificate (Pathstream/Salesforce, 2026): Sales & CRM Overview, Lead & Opportunity Management, Reports & Dashboards, Customer Success.
        - Front-End Web Development Specialization (University of Washington, 2026): HTML/CSS, Responsive Web Layouts, Git & GitHub, AI-enhanced web workflows.
        """,
        """
        TECHNICAL SKILLS & EXPERIENCE:
        - Salesforce Operations: Lead/Pipeline management, Case escalation, Knowledge Base creation, Price Books, Product catalogs, Quote generation, Contracts, Custom Reports/Dashboards.
        - Web Development: WordPress, Elementor, Divi Builder, HTML/CSS, Responsive Layouts.
        - AI & Automation: Python, RAG Systems (ChromaDB + Gemini), Prompt Engineering, AI workflow automation.
        - Experience: Web Designer & Sales at ConnectSolutions.
        """
    ]
    
    metadatas = [
        {"type": "profile_summary"},
        {"type": "web_portfolio"},
        {"type": "salesforce_portfolio"},
        {"type": "certifications"},
        {"type": "skills_and_experience"}
    ]
    
    store.add_documents(texts=user_data, metadatas=metadatas)
    print("User credentials, live web sites, and Salesforce portfolio projects loaded into ChromaDB memory!")

if __name__ == "__main__":
    load_user_credentials()