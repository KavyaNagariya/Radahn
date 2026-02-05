import os 
from google.genai import types

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
    if not valid_target_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_path, 'r', encoding='utf-8') as file:
            MAX_CHARS = 10000
            content = file.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except FileNotFoundError:
        return "Error: File not found."
    except UnicodeDecodeError:
        return "Error: Could not read file encoding."

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of the given file as a string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path to list files from, relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)

