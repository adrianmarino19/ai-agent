import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions
from config import MODEL_ID, client
from cli import get_query_cli


def get_response(query: str) -> types.GenerateContentResponse:
    messages = [types.Content(role="user", parts=[types.Part(text=query)])]
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions], temperature=0
        ),
    )
    return response


def get_metadata(response: types.GenerateContentResponse):
    meta_data = response.usage_metadata

    if not meta_data:
        raise RuntimeError("Please input a valid API Key")
    return meta_data


if __name__ == "__main__":
    user_query, verbose = get_query_cli()
    response = get_response(user_query)

    if verbose:
        meta_data = get_metadata(response)
        print(f"User prompt: {user_query}")
        print(f"Prompt tokens: {meta_data.prompt_token_count}")
        print(f"Response tokens: {meta_data.candidates_token_count}")

    print(f"Response: {response.text}")

    function_call = response.function_calls
    if function_call:
        for function in function_call:
            print(f"Calling function: {function.name}({function.args})")

    # put this all in a function my friend...
    # if   if response.function_calls().name.name and
