import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    raise RuntimeError("Please put a valid API Key...")


client = genai.Client(api_key=api_key)

if __name__ == "__main__":
    main()
