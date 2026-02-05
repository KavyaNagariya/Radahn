import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    # true or false value save hogi in valid_target_dir
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    return get_directory_content(target_dir, directory)


def get_directory_content(target_dir, directory='.'):
    if directory == '.':
        lines = ['Results for current directory:']
    else:
        lines = [f'Results for {directory} directory:']
    dir_content = os.listdir(target_dir)
    try:
        for content in dir_content:
            full_path = os.path.join(target_dir, content)
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            lines.append(f"  - {content}: file_size={file_size} bytes, is_dir={is_dir}")    
    except OSError as e:
        return f"Error accessing directory: {e}"

    return "\n".join(lines)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
