from typing import Any

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file
from config import WORKING_DIR

from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ],
)

FUNCTION_MAP = {
    "get_file_content": get_file_content,
    "write_file": write_file,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
}


def call_function(
    function_call: types.FunctionCall,
    verbose: bool = False,
) -> types.Content:

    function_name = function_call.name or ""

    if not verbose:
        print(f" - Calling function: {function_name}")
    else:
        print(f" - Calling function: {function_name}({function_call.args})")

    if function_name not in FUNCTION_MAP:
        unknown_function = types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
        return unknown_function

    args = dict[str, Any](function_call.args) if function_call.args else {}
    args["working_directory"] = WORKING_DIR

    part = [
        types.Part.from_function_response(
            name=function_name,
            response={"result": FUNCTION_MAP[function_name](**args)},
        )
    ]

    return types.Content(role="tool", parts=part)
