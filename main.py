import os ,sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if len(sys.argv) < 2:
        print("I need a prompt!")
        print("Usage: python main.py 'prompt'")   
        sys.exit(1)
    verbose_flag = False
    if sys.argv[1] == '--verbose':
        verbose_flag = True
        user_prompt = " ".join(sys.argv[2:])
    else:
        user_prompt = " ".join(sys.argv[1:])

    available_functions = types.Tool(
    function_declarations=[schema_get_files_info, 
        schema_get_file_content,
        schema_run_python_file, 
        schema_write_file],
    )
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt), 
    )
    
    if response is None or response.usage_metadata is None:
        print("Response is malformed.")
        return
    
    if verbose_flag:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls:
        for function_call in response.function_calls:
            try:
                function_call_result = call_function(function_call, verbose_flag)
                function_response = function_call_result.parts[0].function_response
                if function_response is None:
                    raise Exception('No response object found')
                if function_response.response is None:
                    raise Exception('No response found')
                print(f"-> {function_response.response['result']}")
            except Exception as e:
                print(f"An exception occured: {e}")       
    else:
        print(response.text)
    
    
main()


