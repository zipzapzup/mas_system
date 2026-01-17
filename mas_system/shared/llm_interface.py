import os
import google.generativeai as genai
from dotenv import load_dotenv

# It's crucial to load environment variables before using them
load_dotenv()

def get_gemini_api_key():
    """
    Retrieves the Gemini API key from environment variables.
    Raises an error if the key is not found.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file. Please add it.")
    return api_key

def configure_gemini():
    """
    Configures the Gemini API with the key.
    """
    try:
        genai.configure(api_key=get_gemini_api_key())
    except ValueError as e:
        print(e)
        # Exit or handle the error as appropriate
        exit(1)

# Call configuration at the module level so it's ready when imported
configure_gemini()

def call_gemini(system_prompt: str, user_prompt: str) -> str:
    """
    Makes a call to the Gemini API with a given system and user prompt.

    Args:
        system_prompt: The role or context for the AI (e.g., "You are a backend developer...").
        user_prompt: The specific task or question for the AI.

    Returns:
        The text response from the Gemini model.
    """
    print(f"--- Calling Gemini ---")
    print(f"System Prompt: {system_prompt[:100]}...")
    print(f"User Prompt: {user_prompt[:100]}...")
    
    # --- THIS IS THE CORE LLM LOGIC ---
    # You would uncomment and complete this section.
    # -----------------------------------
    # model = genai.GenerativeModel('gemini-pro') # Or other suitable model
    #
    # # The Gemini API uses a different format than system/user prompts.
    # # We combine them into a single list of messages.
    # full_prompt = [
    #     {'role': 'user', 'parts': [system_prompt, user_prompt]}
    # ]
    #
    # try:
    #     response = model.generate_content(full_prompt)
    #     print("--- Gemini Response Received ---")
    #     return response.text
    # except Exception as e:
    #     print(f"An error occurred while calling the Gemini API: {e}")
    #     return f"Error: Could not get response from Gemini. Details: {e}"
    # -----------------------------------

    # --- RETURNING A PLACEHOLDER FOR NOW ---
    # Replace this with the actual implementation above.
    print("--- Returning Placeholder (LLM not called) ---")
    placeholder_response = f"""
    {{
        "explanation": "This is a placeholder response because the actual Gemini API was not called.",
        "file_path": "src/components/HelloWorld.tsx",
        "code": "import React from 'react';\n\nconst HelloWorld = () => <h1>Hello, World!</h1>;\n\nexport default HelloWorld;"
    }}
    """
    return placeholder_response
