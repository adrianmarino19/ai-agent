import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function
from config import MODEL_ID, client
from cli import get_query_cli


def get_metadata(response: types.GenerateContentResponse):
    meta_data = response.usage_metadata

    if not meta_data:
        raise RuntimeError("Please input a valid API Key")
    return meta_data


def generate_response(query: str, verbose: bool | None = None) -> str | None:
    messages = [types.Content(role="user", parts=[types.Part(text=query)])]
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions], temperature=0
        ),
    )

    if verbose:
        meta_data = get_metadata(response)
        print(f"User prompt: {query}")
        print(f"Prompt tokens: {meta_data.prompt_token_count}")
        print(f"Response tokens: {meta_data.candidates_token_count}")

    if response.text:
        return f"Response: {response.text}"
    else:
        function_call = response.function_calls
        function_call_result = call_function(function_call)

        final_result = []
        if (
            not function_call_result.parts
            or function_call_result.parts[0].function_response is None
            or function_call_result.parts[0].function_response.response is None
        ):
            raise ValueError("Function call result has no parts")

        final_result.append(function_call_result.parts[0])

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
            return


if __name__ == "__main__":
    query, verbose = get_query_cli()
    response = generate_response(query, verbose)


# The types.Content object that we return from call_function should have a non-empty .parts list. If it doesn't, raise an exception.
# We want to look at the .function_response property of the first item in the list of parts, i.e. .parts[0].function_response. It should be a FunctionResponse object. If it's somehow None, raise an exception.
# Finally, we need to check the .response field of the FunctionResponse object, i.e. .parts[0].function_response.response. This is where the actual function result will be. If it's None, raise an exception.
# Whew! Now that we know that some response came back from the function call, add .parts[0] to a list of function results. We'll use that later.
# If verbose mode is in effect, print the result of the function call like this:
# print(f"-> {function_call_result.parts[0].function_response.response}")
