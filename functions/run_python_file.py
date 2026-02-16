import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_file_path]

        if args:
            command.extend([args])

        result = subprocess.run(
            command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30
        )
        output = []

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"


# Assuming all those checks passed, we're going to use a subprocess to run the file. But first we need to

# Use the subprocess.run() function to run the command that you built. This will return a CompletedProcess object, which you'll want to assign to a variable. Also, when calling subprocess.run(), make sure to provide the necessary arguments to:
# Set the working directory properly.
# Capture output (i.e., stdout and stderr).
# Decode the output to strings, rather than bytes; this is done by setting text=True.
# Set a timeout of 30 seconds to prevent infinite execution.
# Build an output string based on the CompletedProcess object:
# If the process exited with a non-zero returncode, include "Process exited with code X".
# If no output was produced in stdout or stderr (both of which are attributes of CompletedProcess), add "No output produced".
# Otherwise, include any text in stdout prefixed with STDOUT:, and any text in stderr prefixed with STDERR:.
# Return the output string.
