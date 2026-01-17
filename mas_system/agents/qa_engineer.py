import json
from mas_system.shared.llm_interface import call_gemini
from mas_system.prompts import QA_ENGINEER_PROMPT

class QAEngineerAgent:
    def __init__(self):
        pass

    def execute_task(self, file_path: str, code: str) -> list:
        """
        Reviews a file for issues and returns a list of issues found.
        """
        prompt_for_qa = f'{{"file_path": "{file_path}", "code": {json.dumps(code)}}}'
        
        response_text = call_gemini(system_prompt=QA_ENGINEER_PROMPT, user_prompt=prompt_for_qa)
        
        try:
            response_json = json.loads(response_text)
            review = response_json['review']
            return review
        except (json.JSONDecodeError, KeyError) as e:
            print(f"!!! QA Engineer Error: Could not parse LLM response. Error: {e} !!!")
            print(f"LLM Response was:
{response_text}")
            return ["Failed to review the code due to an internal error."]

