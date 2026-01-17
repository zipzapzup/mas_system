import argparse
from agents.project_manager import ProjectManagerAgent

def main():
    parser = argparse.ArgumentParser(description="Run the Multi-Agent System.")
    parser.add_argument("objective", type=str, help="The high-level objective for the MAS.")
    
    args = parser.parse_args()
    
    project_manager = ProjectManagerAgent()
    project_manager.execute_task(args.objective)

if __name__ == "__main__":
    main()
