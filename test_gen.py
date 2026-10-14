import os
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

for model in ["gemini-3.5-flash", "gemini-2.5-flash", "gemini-flash-latest"]:
    try:
        r = client.models.generate_content(model=model, contents="Say hello in one short sentence.")
        print(f"OK   {model}: {r.text}")
    except Exception as e:
        print(f"FAIL {model}: {str(e)[:200]}")