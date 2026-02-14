import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MODEL_ID, client
from cli import get_query_cli


def get_response(query: str) -> types.GenerateContentResponse:
    messages = [
        types.Content(role="user", parts=[types.Part(text=(get_query_cli()[0]))])
    ]
    response = client.models.generate_content(model=MODEL_ID, contents=messages)
    return response


def get_metadata(response: types.GenerateContentResponse):
    try:
        meta_data = response.usage_metadata
        return meta_data
    except Exception:
        raise RuntimeError("Please input a valid API Key")


if __name__ == "__main__":
    user_query, verbose = get_query_cli()
    response = get_response(user_query)

    if verbose:
        meta_data = get_metadata(response)
        print(f"User prompt: {user_query}")
        print(f"Prompt tokens: {meta_data.prompt_token_count}")
        print(f"Response tokens: {meta_data.candidates_token_count}")

    print(f"Response: {response.text}")
