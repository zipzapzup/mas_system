#!/bin/bash
# This script is the main entry point for running the Multi-Agent System from the shell.

# --- Configuration ---
VENV_DIR=".venv"
MAIN_SCRIPT="mas_system.main"

# --- Pre-run Checks ---
# Check if the virtual environment directory exists.
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found at '$VENV_DIR'."
    echo "Please run 'uv venv' and 'uv pip install -r requirements.txt' to set it up."
    exit 1
fi

# Check if an objective was provided.
if [ -z "$1" ]; then
    echo "Usage: ./run.sh \"<your high-level objective>\""
    exit 1
fi

# --- Execution ---
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "Starting the MAS with your objective..."
# Set the REDIS_HOST for local execution and run the main script as a module.
# Pass all command-line arguments as the objective string.
REDIS_HOST=localhost python3 -m $MAIN_SCRIPT "$@"

echo "Task dispatched to Project Manager. Monitor progress in the Web UI or Docker logs."
