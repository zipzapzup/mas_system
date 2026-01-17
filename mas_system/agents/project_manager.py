import json
from mas_system.shared.llm_interface import call_gemini
from mas_system.prompts import PROJECT_MANAGER_PROMPT, PROJECT_NAME_GENERATOR_PROMPT
from mas_system.tasks import app as celery_app
from celery import chain

class ProjectManagerAgent:
    def __init__(self):
        # The constructor is now simpler, as agents are decoupled.
        pass

    def execute_task(self, objective: str):
        """
        Orchestrates the completion of a high-level objective.
        1. Generates a project name from the objective.
        2. Calls an LLM to generate a plan.
        3. Dispatches each step of the plan to a chain of coder and qa agents.
        4. Returns the plan.
        """
        # 1. Generate a project name
        project_name_prompt = f"The user's objective is: '{objective}'"
        project_name = call_gemini(system_prompt=PROJECT_NAME_GENERATOR_PROMPT, user_prompt=project_name_prompt).strip()

        # 2. Generate a plan
        prompt_for_pm = f"The user's objective is: '{objective}'"
        response_text = call_gemini(system_prompt=PROJECT_MANAGER_PROMPT, user_prompt=prompt_for_pm)

        try:
            response_json = json.loads(response_text)
            plan = response_json['plan']
        except (json.JSONDecodeError, KeyError) as e:
            print(f"!!! Project Manager Error: Could not parse LLM response. Error: {e} !!!")
            print(f"LLM Response was:\n{response_text}")
            return None

        # 3. Dispatch tasks
        for task in plan:
            # Create a chain of tasks: coder -> qa
            task_chain = chain(
                celery_app.signature('mas_system.tasks.run_coder', args=[task, project_name], queue='coder_queue'),
                celery_app.signature('mas_system.tasks.run_qa_engineer', queue='qa_queue')
            )
            task_chain.apply_async()
            
        return plan
