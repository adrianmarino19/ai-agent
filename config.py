import os
from google import genai
from dotenv import load_dotenv

MODEL_ID = "gemini-2.5-flash"

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("Please input a valid API Key")

client = genai.Client(api_key=api_key)
