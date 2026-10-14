import os
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)
key = os.getenv("GEMINI_API_KEY")

for label, kwargs in [
	("Gemini Developer API", dict(api_key=key)),
	("Vertex express mode", dict(vertexai=True, api_key=key)),
]:
	print(f"\n=== {label} ===")
	try:
		client = genai.Client(**kwargs)
		names = [m.name for m in client.models.list()]
		flash = [n for n in names if "flash" in n]
		print("OK. Flash models:", flash[:15])
	except Exception as e:
		print("FAILED:", type(e).__name__, str(e)[:300])
