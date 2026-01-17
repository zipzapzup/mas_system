from celery import Celery
import time
import json

# Define the Celery application
# The broker is our Redis service, defined in docker-compose.yml
# The backend is also Redis, used to store task results if needed
app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

# This import is placed here to avoid circular dependencies
from mas_system.agents.project_manager import ProjectManagerAgent

# We'll create a generic coder agent for now
# Later, this could be split into FrontendAgent, BackendAgent, etc.
from mas_system.shared.llm_interface import call_gemini
from mas_system.prompts import CODER_AGENT_PROMPT # We will need to add this prompt

@app.task(name='mas_system.tasks.run_project_manager')
def run_project_manager(objective: str):
    """
    The entry point for the Project Manager agent.
    It takes the user's objective, creates a plan, and delegates tasks.
    """
    print(f"--- Project Manager task received for objective: '{objective}' ---")
    pm = ProjectManagerAgent()
    pm.execute_task(objective)
    return "Project Manager task complete."

@app.task(name='mas_system.tasks.run_coder')
def run_coder(task_description: str):
    """
    The task for a Coder agent.
    It takes a description of a coding task, calls the LLM to generate the code,
    and saves it to the workspace.
    """
    print(f"--- Coder task received: '{task_description}' ---")
    
    # Create the prompt for the LLM
    prompt_for_llm = f"""
    Your task is to complete the following objective: '{task_description}'.
    
    You must return your response as a JSON object with two keys:
    1. "file_path": A string representing the full, relative path for the file in the '/app/workspace/' directory (e.g., 'src/components/Button.tsx').
    2. "code": A string containing the complete, raw source code for that file.
    
    Do not include any other commentary or explanation outside of the JSON object.
    """
    
    # Call the LLM
    response_text = call_gemini(system_prompt=CODER_AGENT_PROMPT, user_prompt=prompt_for_llm)
    
    try:
        # Parse the JSON response
        response_json = json.loads(response_text)
        file_path = f"workspace/{response_json['file_path']}"
        code = response_json['code']
        
        # Save the file
        # In a real system, we'd use a more robust file writing tool
        # For now, we'll write directly. This runs INSIDE the container.
        with open(file_path, "w") as f:
            f.write(code)
            
        print(f"+++ Coder successfully wrote file: {file_path} +++")
        return f"File created: {file_path}"
        
    except (json.JSONDecodeError, KeyError) as e:
        print(f"!!! Coder Error: Could not parse LLM response or key is missing. Error: {e} !!!")
        print(f"LLM Response was:\n{response_text}")
        return "Coder task failed due to invalid LLM response format."

# Set a default queue for tasks that don't have one specified
app.conf.task_default_queue = 'coder_queue'
