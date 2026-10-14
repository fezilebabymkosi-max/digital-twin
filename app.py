import os
import time
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import chromadb

# Force reload of environment variables
load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is missing from your .env file!")
    st.stop()

# Initialize Google GenAI client
client = genai.Client(api_key=api_key)

# Models tried in order. First one that answers is used.
CANDIDATE_MODELS = ["gemini-3.5-flash", "gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]

# Initialize ChromaDB Vector Memory Store
@st.cache_resource
def get_vector_store():
    chroma_client = chromadb.PersistentClient(path="./memory/chroma_db")
    return chroma_client.get_or_create_collection(name="persona_memory")

try:
    collection = get_vector_store()
except Exception:
    collection = None

st.set_page_config(page_title="Digital Twin Workspace", page_icon="🤖")
st.title("Fezile Mkosi — Digital Twin Dashboard")

# Initialize Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Prior Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("Ask your Digital Twin a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # 1. Retrieve Context from ChromaDB Memory
        retrieved_context = ""
        if collection and collection.count() > 0:
            results = collection.query(query_texts=[prompt], n_results=2)
            if results and "documents" in results and results["documents"]:
                retrieved_context = "\n".join(results["documents"][0])

        # 2. Build Grounded Persona Instruction
        system_instruction = f"""
You are the Digital Twin of Fezile Mkosi (Salesforce Operations Specialist & WordPress Web Designer).
Answer in the first person ("I") based on this background context:

--- PERSONA CONTEXT ---
{retrieved_context if retrieved_context else "No specific vector store documents returned. Answer professionally as Fezile."}
-----------------------
"""

                # 3. Model call with retries, fallback and full error reporting
        response_text = None
        errors = []

        for model_id in CANDIDATE_MODELS:
            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model=model_id,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction
                        ),
                    )
                    response_text = response.text
                    break
                except Exception as e:
                    msg = str(e)
                    errors.append(f"{model_id} (try {attempt + 1}): {msg[:150]}")
                    # Only retry on temporary overload / rate limit
                    if "503" in msg or "UNAVAILABLE" in msg or "429" in msg:
                        time.sleep(2 * (attempt + 1))
                        continue
                    break  # permanent error (e.g. 404): go to next model
            if response_text:
                break

        if response_text:
            message_placeholder.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        else:
            st.error("All models failed:\n\n" + "\n\n".join(errors))