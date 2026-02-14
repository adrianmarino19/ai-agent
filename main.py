import os
import sys

from dotenv import load_dotenv
from google import genai

from utils import MODEL_ID

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("Please input a valid API Key")


client = genai.Client(api_key=api_key)


response = client.models.generate_content(
    model=MODEL_ID,
    contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
)

if __name__ == "__main__":
    print(response.text)
