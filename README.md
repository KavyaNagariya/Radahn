# Radahn

Radahn is an AI-powered coding assistant CLI tool that uses Google's Gemini AI to help automate coding tasks. It allows an AI agent to safely interact with your codebase through a controlled set of file system operations.

## Features

- **AI-Powered Assistance**: Leverages Google's Gemini 2.5 Flash model to understand and execute coding requests
- **Secure File Operations**: All file access is constrained to a specific working directory for security
- **Function Calling**: Uses structured function calling to enable the AI to:
  - List files and directories with metadata
  - Read file contents (with size limits)
  - Write and overwrite files
  - Execute Python files with optional arguments
- **Interactive CLI**: Simple command-line interface with verbose mode for debugging

## Installation

1. Clone the repository
2. Install dependencies using `uv`:
   ```bash
   uv pip install -e .
   ```
3. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

Run Radahn with a prompt:
```bash
python main.py "your coding request here"
```

Enable verbose mode to see token usage and function calls:
```bash
python main.py --verbose "your coding request"
```

## Example

The repository includes a sample calculator project in the `calculator/` directory. You can test Radahn by asking it to analyze or modify this project:

```bash
python main.py "Analyze the calculator project and run its tests"
```

## Architecture

- `main.py`: Entry point that manages the conversation loop with Gemini AI
- `call_function.py`: Routes function calls to the appropriate handlers
- `prompts.py`: System prompt defining the AI's capabilities
- `functions/`: Contains implementations for each available operation:
  - `get_files_info.py`: Directory listing
  - `get_file_content.py`: File reading
  - `write_file.py`: File writing
  - `run_python_file.py`: Python execution

## Requirements

- Python 3.12+
- Google Gemini API key

## Dependencies

- `google-genai==1.12.1` - Google's Generative AI client
- `python-dotenv==1.1.0` - Environment variable management

## Security

- All file operations are sandboxed to the working directory (`./calculator` by default)
- Path traversal attacks are prevented through validation
- Maximum file read size is limited to 10,000 characters

## License

[Add your license here]
