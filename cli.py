# cli.py

import typer
from orchestrator_agent import handle_user_input, AGENTS
from rich import print
import json
from utils.memory import shared_memory

app = typer.Typer()



@app.command()
def mem():
    """Displays all items currently in the shared memory."""
    print("\n[bold]🧠 Current Memory:[/bold]")
    all_memory = shared_memory.all()
    if not all_memory:
        print("[yellow]Memory is empty.[/yellow]")
        return
    for k, v in all_memory.items():
        # Convert complex objects to string for display
        display_v = str(v)
        print(f"  [green]{k}[/green]: {display_v[:200]}...")

@app.command()
def clear_mem():
    """Clears all items from the shared memory."""
    shared_memory.clear()
    print("[yellow]✅ Memory cleared.[/yellow]")

# @app.command()
# def mem():
#     print("\n[bold]Memory:[/bold]")
#     for k, v in memory.all().items():
#         print(f"[green]{k}[/green]: {v[:200]}...")

# @app.command()
# def clear():
#     memory.clear()
#     print("[yellow]Memory cleared.[/yellow]")

# import re
# def format_recursively(data, context):
#     """Recursively formats strings in a nested data structure, safely ignoring
#     placeholders that are not in the context."""
#     if isinstance(data, dict):
#         return {k: format_recursively(v, context) for k, v in data.items()}
#     elif isinstance(data, list):
#         return [format_recursively(item, context) for item in data]
#     elif isinstance(data, str):
#         placeholders = re.findall(r"\{\{(.*?)\}\}", data)
#         for placeholder in placeholders:
#             if placeholder in context:
#                 data = data.replace(f"{{{{{placeholder}}}}}", str(context[placeholder]))
#         return data
#     else:
#         return data

@app.command()
def chat():
    print("[bold green]Multi-Agent CLI[/bold green]")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("🧠 You: ")
        if user_input.strip().lower() in ("exit", "quit"):
            break
        response = handle_user_input(user_input)
        print(f"\n🤖 [bold cyan]Response:[/bold cyan] {response}\n")

# Replace the old 'agent' function with this one in cli.py

@app.command()
def agent(
    agent_id: str,
    inputs: list[str] = typer.Argument(
        ..., help="Inputs for the agent in 'key=value' format."
    ),
):
    """
    Calls a specific agent with dynamic key-value inputs.
    """
    if agent_id not in AGENTS:
        print(f"[bold red]❌ Agent not found: {agent_id}[/bold red]")
        raise typer.Exit()

    # Assemble the key-value pairs from the command line into a dictionary
    input_dict = {}
    for item in inputs:
        if "=" not in item:
            print(f"[bold red]Invalid input: '{item}'. Use 'key=value'.[/bold red]")
            raise typer.Exit()
        key, value = item.split("=", 1)
        input_dict[key] = value

    print(f"🤖 Calling [bold blue]{agent_id}[/bold blue] with inputs: {input_dict}")
    
    # Run the agent with the structured dictionary input
    output = AGENTS[agent_id].run(input_dict)
    print(f"\n📄 [bold cyan]{agent_id} Output:[/bold cyan]\n{output}")

@app.command()
def file(agent_id: str, file_path: str):
    with open(file_path, "r") as f:
        content = f.read()
    output = AGENTS[agent_id].run(content)
    print(f"\n📄 [bold cyan]{agent_id} Output:[/bold cyan] {output}")

@app.command()
def json_input(file_path: str):
    with open(file_path) as f:
        input_data = json.load(f)
    output = handle_user_input(input_data)
    print(f"\n🧠 [bold cyan]Output:[/bold cyan] {output}")


    # Add this new command inside cli.py

@app.command()
def workflow(
    workflow_file: str,
    context_vars: list[str] = typer.Argument(
        None, help="Dynamic inputs for the workflow in 'key=value' format."
    ),
):
    """
    Runs a workflow from a JSON file with dynamic, overrideable inputs.
    """
    try:
        with open(workflow_file) as f:
            # The structure from the file is {"input": {...}}
            data = json.load(f).get("input", {})
    except FileNotFoundError:
        print(f"[bold red]Error: Workflow file not found at '{workflow_file}'[/bold red]")
        raise typer.Exit()

    # Override context with variables from the command line
    if context_vars:
        for var in context_vars:
            if "=" not in var:
                print(f"[bold red]Invalid format: '{var}'. Use 'key=value'.[/bold red]")
                continue
            key, value = var.split("=", 1)
            data[key] = value
            print(f"[bold yellow]Overriding context: {key}='{value[:30]}...'[/bold yellow]")

    # Pass the final combined dictionary to the orchestrator
    output = handle_user_input(data)
    print(f"\n🧠 [bold cyan]Workflow Output:[/bold cyan]")
    print(output)

if __name__ == "__main__":
    app()


# to run
# python cli.py chat

# # Or use:
# python cli.py agent resume_analyzer_agent "Review this resume..."
# python cli.py file code_explainer_agent sample.py
# python cli.py json_input resume_chain_input.json


# python cli.py mem
# python cli.py clear
