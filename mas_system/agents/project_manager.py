from .database_agent import DatabaseAgent
from .backend_agent import BackendAgent
from .frontend_agent import FrontendAgent

class ProjectManagerAgent:
    def __init__(self):
        # In a real system, these might be initialized on demand
        self.database_agent = DatabaseAgent()
        self.backend_agent = BackendAgent()
        self.frontend_agent = FrontendAgent()

    def execute_task(self, objective):
        print(f"Project Manager: Received objective - '{objective}'")
        
        # 1. Simulate planning phase
        print("\nProject Manager: Analyzing objective and creating a plan...")
        plan = [
            "1. Design database schema for users and articles.",
            "2. Create backend API endpoints for user authentication and article CRUD.",
            "3. Build frontend components for displaying articles and user login."
        ]
        print("Project Manager: Plan created.")
        for step in plan:
            print(f"- {step}")

        # 2. Simulate delegation to specialized agents
        print("\nProject Manager: Delegating tasks to specialized agents...")

        # Delegate to DatabaseAgent
        schema_task = "A schema for 'users' (email, password) and 'articles' (title, content, author_id)"
        sql_schema = self.database_agent.design_schema(schema_task)
        print(f"Project Manager: Received artifact from Database Agent: \n---\n{sql_schema}\n---\n")

        # Delegate to BackendAgent
        endpoint_task = "CRUD endpoints for /api/articles"
        api_code = self.backend_agent.create_endpoint(endpoint_task)
        print(f"Project Manager: Received artifact from Backend Agent: \n---\n{api_code}\n---\n")

        # Delegate to FrontendAgent
        component_task = "A React component to display a list of articles"
        component_code = self.frontend_agent.create_component(component_task)
        print(f"Project Manager: Received artifact from Frontend Agent: \n---\n{component_code}\n---\n")

        print("\nProject Manager: All tasks completed. Project build is finished.")
