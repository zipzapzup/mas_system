import json
from mas_system.shared.llm_interface import call_gemini
from mas_system.prompts import PROJECT_MANAGER_PROMPT
from mas_system.tasks import run_coder

class ProjectManagerAgent:
    def __init__(self):
        # The constructor is now simpler, as agents are decoupled.
        pass

    def execute_task(self, objective: str):
        """
        Orchestrates the completion of a high-level objective.
        1. Calls an LLM to generate a plan.
        2. Dispatches each step of the plan to the coder queue.
        """
        print(f"--- Project Manager received objective: '{objective}' ---")

        # 1. Call the LLM to generate a plan
        print("...Calling LLM to generate a project plan...")
        prompt_for_pm = f"The user's objective is: '{objective}'"
        response_text = call_gemini(system_prompt=PROJECT_MANAGER_PROMPT, user_prompt=prompt_for_pm)

        # 2. Parse the plan from the LLM's JSON response
        try:
            response_json = json.loads(response_text)
            plan = response_json['plan']
            print(f"+++ Plan generated successfully with {len(plan)} steps +++")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"!!! Project Manager Error: Could not parse LLM response or 'plan' key is missing. Error: {e} !!!")
            print(f"LLM Response was:\n{response_text}")
            return # Stop execution if the plan is invalid

        # 3. Dispatch tasks to the coder queue
        print("...Dispatching tasks to Coder Agents...")
        for i, task in enumerate(plan):
            print(f"Dispatching task {i+1}/{len(plan)}: {task}")
            # This sends the task to the 'coder_queue' for a Coder Agent to pick up
            run_coder.apply_async(args=[task], queue='coder_queue')

        print("--- All tasks dispatched. Project Manager's job is complete. ---")
        print("--- Coder Agents are now working on the tasks. ---")
