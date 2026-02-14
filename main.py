import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentResponse

from config import MODEL_ID, client
from cli import get_query_cli


def get_response(query: str) -> GenerateContentResponse:
    response = client.models.generate_content(model=MODEL_ID, contents=query)
    return response


def get_metadata(response: GenerateContentResponse):
    try:
        meta_data = response.usage_metadata
        return meta_data
    except Exception:
        raise RuntimeError("Please input a valid API Key")


if __name__ == "__main__":
    user_query = get_query_cli()
    response = get_response(user_query)
    meta_data = get_metadata(response)

    if meta_data:
        print(f"Prompt tokens: {meta_data.prompt_token_count}")
        print(f"Response tokens: {meta_data.candidates_token_count}")
        print(f"Response: {response.text}")
