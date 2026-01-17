# Multi-Agent System Framework

This directory contains a basic framework for a Multi-Agent System (MAS) designed to build full-stack web applications.

## Architecture

- **`main.py`**: The entry point for the system. It takes a user's objective and passes it to the Project Manager Agent.
- **`agents/`**: This directory contains the code for each specialized agent.
  - `project_manager.py`: The orchestrator that breaks down tasks and delegates them.
  - `frontend_agent.py`: Responsible for generating UI code.
  - `backend_agent.py`: Responsible for generating API and server-side logic.
  - `database_agent.py`: Responsible for designing database schemas.
- **`prompts.py`**: Stores the detailed system prompts that define the role and capabilities of each agent.
- **`shared/`**: A directory for any utility functions or shared code (e.g., functions to call an LLM).

## How it Works

1.  A user provides a high-level objective via the command line to `main.py`.
2.  The `ProjectManagerAgent` receives this objective.
3.  It uses an LLM (guided by the `PROJECT_MANAGER_PROMPT`) to create a step-by-step plan.
4.  For each step, it generates a specific prompt and delegates the task to the appropriate specialized agent (e.g., `FrontendAgent`).
5.  The specialized agent uses an LLM (guided by its own specific prompt) to generate the required artifact (e.g., code, schema).
6.  The generated artifacts are saved to the file system.

## Usage

To run the system, you would use the following command from the root of the repository:

```bash
python mas_system/main.py "Your high-level objective for the web application"
```
