import os, subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        if not valid_target_path:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        command = ['python', target_path]
        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = []
        if result.returncode != 0:
            output.append(f'Process exited with code {result.returncode}')
        if not result.stdout and not result.stderr:
            output.append('No output produced')
        if result.stdout:
            return f'STDOUT:\n{result.stdout}'
        if result.stderr:
            return f'STDERR:\n{result.stderr}'
        return '\n'.join(output)
    except Exception as e:
        return f'Error: executing Python file: {e}'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Reads file in a specified directory relative to the working directory, providing file content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Runs a python file with the python3 interpreter. Accepts additional CLI args as an optional array.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional array of strings to be used as the CLI args for the Python file.",
                items=types.Schema(
                    type=types.Type.STRING,
                )
            ),
        },
        required=["file_path"]
    ),
)