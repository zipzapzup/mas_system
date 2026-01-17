# How to Run the Multi-Agent System

This document provides step-by-step instructions on how to set up and run this multi-agent system (MAS).

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker and Docker Compose**: For running the containerized services.
- **Python 3.11+**: For running the local scripts.
- **uv**: For Python package and environment management. You can install it with `pip install uv`.

## 1. Initial Setup

### a. Clone the Repository

If you haven't already, clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

### b. Create the Environment File

The system uses a `.env` file to manage secret keys, such as your Gemini API key. Create a `.env` file in the root of the project:

```bash
cp .env.example .env
```

Now, open the `.env` file and add your `GEMINI_API_KEY`.

### c. Set Up the Virtual Environment

This project uses `uv` to manage an isolated Python environment.

1.  **Create the virtual environment:**
    ```bash
    uv venv
    ```
    This will create a `.venv` directory in the project root.

2.  **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

## 2. Running the System

### a. Start the Docker Services

All the agent services, along with Redis and Mongo, are managed by Docker Compose. To start them, run:

```bash
docker compose up --build -d
```
This command builds the Docker images and starts all services in detached mode.

### b. Activate the Virtual Environment

Before running the main script, you must activate the local Python virtual environment:

```bash
source .venv/bin/activate
```

### c. Run an Objective

Now you can give the MAS an objective by running the `main.py` script. The script must be run as a module from the project's root directory, and you need to set the `REDIS_HOST` environment variable.

```bash
REDIS_HOST=localhost python3 -m mas_system.main "Your high-level objective here"
```

**Example:**
```bash
REDIS_HOST=localhost python3 -m mas_system.main "Create a simple Flask application with a single endpoint that returns 'Hello, World!'"
```

## 3. Observing the System

You can monitor the activity of the agents in two ways:

### a. Web UI

A web-based user interface is available to view the operational logs in real-time. Access it in your browser at:

**http://localhost:5001**

The page will auto-refresh every 5 seconds.

### b. Docker Logs

To see the raw, real-time logs from all running services, you can use:

```bash
docker compose logs -f
```

## 4. Stopping the System

To stop all the running Docker containers, use the following command:

```bash
docker compose down
```

This will stop and remove the containers, but your data in the `workspace/`, `redis_data/`, and `mongo_data/` volumes will be preserved.
