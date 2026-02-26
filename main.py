import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_CHARS, MODEL_ID, MAX_ITERS, client
from cli import get_query_cli


def get_metadata(response: types.GenerateContentResponse):
    meta_data = response.usage_metadata

    if not meta_data:
        raise RuntimeError("Please input a valid API Key")
    return meta_data


def generate_response(
    query: str,
    messages: list[types.Content],
    verbose: bool | None = None,
) -> str | None:

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions], temperature=0
        ),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API is malformed")

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if verbose:
        meta_data = get_metadata(response)
        print(f"User prompt: {query}")
        print(f"Prompt tokens: {meta_data.prompt_token_count}")
        print(f"Response tokens: {meta_data.candidates_token_count}")

    if not response.function_calls:
        return f"Response: {response.text}"

    function_responses = []
    for function_call in response.function_calls:
        result = call_function(function_call, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])

    messages.append(types.Content(role="user", parts=function_responses))
    # TODO: return or use function_responses (e.g. send back to model and recurse/loop)
    return None


def run_agent(client, messages, verbose):
    for _ in range(MAX_ITERS):
        try:
            final_response = generate_response(client, messages, verbose)
            if final_response:
                print("Final result:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generating content: {e}")


def main():
    query, verbose = get_query_cli()
    messages = [types.Content(role="user", parts=[types.Part(text=query)])]
    run_agent(client, messages, verbose)


if __name__ == "__main__":
    main()
