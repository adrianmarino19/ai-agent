from typing import Any


from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

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
    function_call: list[types.FunctionCall],
    verbose: bool = False,
) -> types.Content:
    function_result = []

    for function in function_call:
        if function.name in FUNCTION_MAP:
            function_name = function.name or ""
            function_args = dict[str, Any](function.args) if function.args else {}
            function_args["working_directory"] = "./calculator"

            if not verbose:
                print(f" - Calling function: {function.name}")
            else:
                print(f"Calling function: {function.name}({function.args})")

            function_result.append(FUNCTION_MAP[function_name](**function_args))

            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result},
                    )
                ],
            )

        # So this can only call one function....

        else:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )


# return types.Content(
#     role="tool",
#     parts=[
#         types.Part.from_function_response(
#             name=function_name,
#             response={"error": f"Unknown function: {function_name}"},
#         )
#     ],
# )
