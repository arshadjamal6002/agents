from adk import LlmAgent
from orchestrator_agent import AGENTS
from utils.memory import shared_memory

def format_recursively(data, context):
    """Recursively formats strings in a nested data structure (dicts, lists)."""
    if isinstance(data, dict):
        # If it's a dictionary, format each value
        return {k: format_recursively(v, context) for k, v in data.items()}
    elif isinstance(data, list):
        # If it's a list, format each item
        return [format_recursively(item, context) for item in data]
    elif isinstance(data, str):
        # If it's a string, try to format it with the context
        return data.format(**context)
    else:
        # Return data of other types as-is
        return data

class WorkflowAgent(LlmAgent):
    def run(self, input):
        steps = input.get("steps", [])
        context = input.copy()

        print(f"[Workflow] Starting with initial context: {list(context.keys())}")

        for idx, step in enumerate(steps):
            agent_name = step["agent"]
            task_input = step["input"]

            # Create a combined dictionary of step-specific context AND shared memory
            full_context = {**shared_memory.all(), **context}
            formatted_input = format_recursively(task_input, full_context)

            agent = AGENTS.get(agent_name)
            if not agent:
                return {"error": f"Unknown agent: {agent_name}"}

            print(f"--- [Workflow] Step {idx+1}: Running {agent_name} ---")
            output = agent.run(formatted_input)

            output_key = step.get("output_key", f"output_{idx+1}")
            context[output_key] = output
            shared_memory.store(output_key, output) # 🧠 Save to shared memory

            print(f"--- [Workflow] Step {idx+1} complete. Saved output to '{output_key}' ---")

        return context

agent = WorkflowAgent()
