# Digital Twin & Personal Assistant Engine

An interactive command-line assistant built with Python, Google GenAI SDK (Gemini), and ChromaDB. 

The system uses local vector storage (ChromaDB) to ground responses directly in verified portfolio details (Salesforce Operations, WordPress web design, and Python tools).

---

## Features

* **Grounded Memory Retrieval:** Reads local background files to ensure proposal outputs reference actual live projects (`oasis.org.za`, `cipa.org.za`) and real Salesforce experience.
* **Multi-Mode CLI:**
  * `pitch`: Generates tailored Upwork/client proposals based on job descriptions.
  * `plan`: Formats raw daily notes into actionable task lists and revenue routes.
  * `general`: Handles standard queries.
* **Model Fallback:** Automatically switches from `gemini-3.8-flash` to `gemini-2.5-flash` if primary endpoints experience high traffic.

---

## Project Structure