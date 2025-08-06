🧠 GenAI Multi-Agent Orchestration Framework
A full-stack, production-ready framework for building, testing, and deploying sophisticated AI systems where multiple agents collaborate to solve complex problems.
Welcome to a new paradigm of AI application development. This framework moves beyond single-purpose AI tools to a cohesive ecosystem where specialized agents work in concert, orchestrated by a central intelligence and accessible through a rich suite of interfaces. From backend API to a polished web UI, this project provides every component needed to bring advanced agentic workflows to life.

## 📜 Table of Contents
Core Philosophy

Features at a Glance

System Architecture

Technology Stack

🚀 Getting Started: A Step-by-Step Guide

💻 A Tour of the System: How to Use It

Testing the Core Components

Running the Full System

Interacting via the REST API

Using the Command-Line Interface (CLI)

Using the Streamlit Web UI

🤖 The Agent Roster

🗺️ Future Roadmap

🤝 How to Contribute

## 🎯 Core Philosophy
This framework is built on three key principles:

🧩 Modularity: Each component—from individual agents to the UI—is decoupled and self-contained. This makes the system easy to extend, test, and maintain. Adding a new AI capability is as simple as creating a new agent.

🧪 Testability: A system is only as good as its reliability. With a built-in evaluation suite, you can create repeatable tests to validate agent performance and ensure that new changes don't break existing functionality.

🤝 Usability: Powerful AI should be accessible. With a REST API, an interactive CLI, and a polished Streamlit UI, the system caters to developers, testers, and end-users alike, making it perfect for both development and demonstration.

## ✨ Features at a Glance
Feature

Description

Status

Modular Agent Architecture

Plug-and-play structure for adding new, specialized AI agents.

✅

LLM-Powered Orchestrator

A central routing agent that understands natural language and delegates tasks to the correct specialist.

✅

Multi-Agent Workflows

A meta-agent that executes complex, multi-step tasks by chaining other agents together in sequence.

✅

Persistent Shared Memory

A file-backed memory (memory.json) allows agents to share context and state across different runs and sessions.

✅

REST API

A robust FastAPI backend that exposes all agents and the orchestrator through clean, documented endpoints.

✅

Interactive CLI

A powerful command-line interface built with Typer for rapid testing, scripting, and direct interaction.

✅

Streamlit Web UI

A feature-rich, user-friendly web interface for demos and interactive use, complete with a live prompt editor and workflow builder.

✅

Live Prompt Engineering

The web UI includes a sidebar to edit and save agent master prompts on-the-fly for the current session.

✅

YAML-Based Evaluation

A simple but effective testing suite to run predefined test cases against your agents and validate their outputs.

✅

## 🏗️ System Architecture
The framework is designed with a clear separation of concerns, enabling scalability and maintainability.

graph TD
    subgraph User Interfaces
        A[🌐 Streamlit Web UI]
        B[💻 Command-Line (CLI)]
        C[🔌 External Apps]
    end

    subgraph Core System
        D[🚀 FastAPI Server]
        E[🧠 Orchestrator Agent]
        F[🔄 Workflow Agent]
    end

    subgraph Specialist Agents
        G[📄 Doc QA Agent]
        H[✉️ Email Agent]
        I[💻 Code Explainer]
        J[📊 SQL Generator]
        K[...]
    end

    subgraph Shared State
        L[🧠 Shared Memory (memory.json)]
    end

    A --> D
    B --> D
    C --> D

    D --> E
    D -- Direct Call --> F
    D -- Direct Call --> G
    D -- Direct Call --> H
    D -- Direct Call --> I
    D -- Direct Call --> J
    D -- Direct Call --> K

    E -- Routes to --> G
    E -- Routes to --> H
    E -- Routes to --> I
    E -- Routes to --> J
    E -- Routes to --> K

    F -- Executes --> G
    F -- Executes --> H
    F -- Executes --> I
    F -- Executes --> J
    F -- Executes --> K

    F -- Writes to --> L
    G -- Can Read/Write --> L
    H -- Can Read/Write --> L
    I -- Can Read/Write --> L
    J -- Can Read/Write --> L
    K -- Can Read/Write --> L

## 🛠️ Technology Stack
Backend: Python 3.10+, FastAPI, Uvicorn

AI/LLM: LangChain, OpenAI

CLI: Typer, Rich

Web UI: Streamlit

Tooling: python-dotenv, PyYAML

## 🚀 Getting Started: A Step-by-Step Guide
1. Prerequisites
Python 3.10 or newer.

An OpenAI API key.

2. Installation & Setup
Clone the Repository

git clone <your-repo-url>
cd <your-project-directory>

Create and Activate a Virtual Environment

# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install Dependencies

pip install -r requirements.txt

Configure Your API Key

Create a new file named .env in the root directory.

Add your OpenAI API key to this file:

OPENAI_API_KEY="sk-..."

## 💻 A Tour of the System: How to Use It
This framework is designed to be tested and used at every level.

Testing the Core Components
Before running the full application, you can test individual agents and the orchestrator using the provided scripts.

Test the Orchestrator's Routing Logic:

python -m scripts.test_orchestrator

Test a Specific Agent (e.g., Code Explainer):

python -m scripts.test_code_explainer

Run the Full Evaluation Suite: This runs all the test cases defined in evaluations/tests.yaml and saves trace logs.

python -m evaluations.eval_runner

Running the Full System
To use the UI or API, you must have the backend server running.

Start the Backend API Server: Open a terminal and run:

uvicorn api_server:app --reload

The API is now live at http://localhost:8000. Keep this terminal running.

Interacting via the REST API
Use curl or any API client to interact with the backend.

Call the Orchestrator with a Structured Input:

curl -X POST http://localhost:8000/instruct -H "Content-Type: application/json" -d "{\"input\": {\"code\": \"def hello_world():\\n  print(\\\"Hello, World!\\\")\", \"language\": \"Python\", \"depth\": \"beginner\"}}"

Run a Workflow from a JSON File:

curl -X POST http://localhost:8000/agent/workflow_agent -H "Content-Type: application/json" --data @test_workflow.json

Using the Command-Line Interface (CLI)
Open a second terminal to use the CLI while the API server is running.

Start an Interactive Chat with the Orchestrator:

python cli.py chat

Call a Specific Agent with Dynamic Inputs:

python cli.py agent sql_generator_agent "instruction=Get all users from India" "table_schema=CREATE TABLE users (id INT, name TEXT, country TEXT);" "sql_dialect=Standard SQL"

Run a Workflow and Override Context Variables:

python cli.py workflow test_workflow.json "resume=Arshad Jamal, a skilled Cloud Engineer with 5 years experience in AWS and Terraform." "job_description=We are hiring a DevOps professional with strong AWS and Infrastructure-as-Code skills."

Inspect the Shared Memory:

python cli.py mem

Using the Streamlit Web UI
This is the most intuitive way to use the system.

Start the UI: In your second terminal, run:

streamlit run ui.py

A browser tab will open with the application, where you can use the interactive chaining UI, prompt editor, and all other features.

## 🤖 The Agent Roster
The framework comes with a suite of pre-built agents. Add your own by creating a new folder in the agents/ directory.

Agent Name

Required Inputs

Description

code_explainer_agent

code, language, depth

Explains code snippets in detail.

doc_qa_agent

pdf_path, question

Answers questions from a provided PDF document.

email_generator_agent

purpose, content, tone

Generates professional email drafts.

resume_analyzer_agent

resume_text, job_description

Analyzes a resume against a job description.

slide_generator_agent

topic, bullets

Creates presentation outlines.

sql_generator_agent

instruction, table_schema, sql_dialect

Generates SQL queries from natural language.

workflow_agent

steps (list), initial context (e.g., resume)

Meta-Agent: Executes a chain of other agents.

## 🗺️ Future Roadmap
[ ] Enhanced Logging & Trace Viewer: Implement a robust logging system and a UI to visualize the step-by-step execution of agent workflows.

[ ] Deployment Packaging: Create Dockerfiles and deployment scripts for easy hosting on platforms like Hugging Face Spaces or cloud services.

[ ] Vector-Based Memory: Upgrade the memory system to use a vector database (e.g., ChromaDB, Pinecone) for long-term, semantic memory retrieval.

[ ] Add More Agents: Continuously expand the system's capabilities by adding new specialist agents for different domains.

## 🤝 How to Contribute
Contributions are welcome! Please feel free to open an issue or submit a pull request.

Fork the repository.

Create a new branch (git checkout -b feature/YourFeature).

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/YourFeature).

Open a Pull Request.