from celery import Celery
import json
import datetime

import os

# Get Redis host from environment variable, default to 'redis' for container environment
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")

# Define the Celery application
app = Celery('tasks', broker=f'redis://{REDIS_HOST}:6379/0', backend=f'redis://{REDIS_HOST}:6379/0')

# Path for the log file inside the container's shared workspace
LOG_FILE_PATH = "/app/workspace/operational_log.md"

def log_to_markdown(title: str, content: dict):
    """Appends a log entry to the operational log file in Markdown format."""
    with open(LOG_FILE_PATH, "a") as f:
        f.write(f"### {title}\n")
        f.write(f"**Timestamp:** `{datetime.datetime.now().isoformat()}`\n\n")
        for key, value in content.items():
            # Format keys to be bold and title-cased
            f.write(f"**{key.replace('_', ' ').title()}:**\n")
            
            # Handle different value types for nice formatting
            if isinstance(value, list):
                for item in value:
                    f.write(f"- {item}\n")
            elif isinstance(value, str) and '\n' in value:
                # Use code blocks for multi-line strings (like code)
                f.write(f"```\n{value}\n```\n")
            else:
                f.write(f"`{value}`\n")
            f.write("\n")
        f.write("---\n\n")

@app.task(name='mas_system.tasks.run_project_manager')
def run_project_manager(objective: str):
    """
    The entry point for the Project Manager agent.
    Logs the objective, creates a plan, logs the plan, and delegates tasks.
    """
    log_to_markdown("Project Manager Task Started", {"Objective": objective})
    
    from mas_system.agents.project_manager import ProjectManagerAgent
    
    pm = ProjectManagerAgent()
    plan = pm.execute_task(objective)
    
    if plan:
        log_to_markdown("Project Manager Plan Generated", {"Plan": plan})
    else:
        log_to_markdown("Project Manager Task Failed", {"Reason": "Could not generate a plan from the LLM."})
        
    return "Project Manager task complete."

@app.task(name='mas_system.tasks.run_coder')
def run_coder(task_description: str, project_name: str):
    """
    The task for a Coder agent.
    Generates one or more files based on a task description.
    """
    log_to_markdown("Coder Task Started", {"Task": task_description, "Project": project_name})

    from mas_system.shared.llm_interface import call_gemini
    from mas_system.prompts import CODER_AGENT_PROMPT

    prompt_for_llm = f"Your task is to complete the following objective: '{task_description}'."
    response_text = call_gemini(system_prompt=CODER_AGENT_PROMPT, user_prompt=prompt_for_llm)
    
    try:
        response_json = json.loads(response_text)
        files_to_create = response_json['files']
        
        created_files = []
        for file_info in files_to_create:
            file_path_in_project = file_info['file_path']
            full_path = os.path.join("/app/workspace", project_name, file_path_in_project)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            code = file_info['code']
            with open(full_path, "w") as f:
                f.write(code)
            
            log_path = os.path.join(project_name, file_path_in_project)
            log_to_markdown("Coder Task: File Created", {"File Path": log_path, "Code": "```\n" + code + "\n```"})
            created_files.append((full_path, code))
            
        return created_files
        
    except (json.JSONDecodeError, KeyError) as e:
        log_to_markdown("Coder Task Failed", {
            "Error": "Could not parse LLM response or 'files' key is missing.",
            "Exception": str(e),
            "LLM Response": response_text
        })
        raise

@app.task(name='mas_system.tasks.run_qa_engineer')
def run_qa_engineer(coder_results):
    """
    The task for a QA Engineer agent.
    Receives a list of file tuples from the coder task and reviews each one.
    """
    log_to_markdown("QA Engineer Task Started", {"Files to Review": f"{len(coder_results)} file(s)"})
    
    from mas_system.agents.qa_engineer import QAEngineerAgent
    qa = QAEngineerAgent()
    
    all_issues = []
    for file_path, code in coder_results:
        review_issues = qa.execute_task(file_path, code)
        if review_issues:
            all_issues.extend(review_issues)
            log_to_markdown("QA Review: Issues Found", {"File": file_path, "Issues": review_issues})
            
    if not all_issues:
        log_to_markdown("QA Engineer Review Complete", {"Status": "No issues found in any files."})
        
    return "QA Engineer task complete."


# Set a default queue for tasks that don't have one specified
app.conf.task_default_queue = 'coder_queue'
