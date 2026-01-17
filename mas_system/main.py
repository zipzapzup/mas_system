import argparse
from mas_system.tasks import run_project_manager

def main():
    """
    This is the main entry point for the user to start the MAS.
    It takes a command-line objective and dispatches it as the first
    task to the Project Manager's queue.
    """
    parser = argparse.ArgumentParser(description="Run the Multi-Agent System.")
    parser.add_argument("objective", type=str, help="The high-level objective for the MAS.")
    
    args = parser.parse_args()
    
    print(f"Objective received: '{args.objective}'")
    print("Dispatching task to Project Manager...")
    
    # This sends the task to the 'project_manager_queue' defined in docker-compose.yml
    run_project_manager.apply_async(args=[args.objective], queue='project_manager_queue')
    
    print("Task dispatched successfully. The agents are now working.")
    print("You can monitor the agent activity by running 'docker-compose logs -f'.")

if __name__ == "__main__":
    main()
