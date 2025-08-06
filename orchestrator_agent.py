# orchestrator_agent.py

import importlib
import json
from typing import Dict, Any
from utils.router import choose_agent
from utils.input_adapter import adapt_input_to_agent
from utils.memory import shared_memory

# Load the agents from config
with open("config/agents_manifest.json") as f:
    AGENT_CONFIGS = json.load(f)

AGENTS = {}

# Dynamically import all agents
for agent in AGENT_CONFIGS:
    module_path = agent["path"]  # e.g., "agents.doc_qa_agent.agent"
    module = importlib.import_module(module_path)
    AGENTS[agent["name"]] = module.agent  # assumes each agent exports `agent`

def handle_user_input(user_input: str | Dict[str, Any]) -> Dict[str, Any]:
    """
    Orchestrator entry point.
    Accepts user input, routes to agent, returns output.
    """
    try:
        # Determine routing input text
        if isinstance(user_input, str):
            task_input = user_input
        elif isinstance(user_input, dict):
            task_input = json.dumps(user_input)
        else:
            return {"error": "Invalid input format."}

        selected_agent_name = choose_agent(task_input, AGENT_CONFIGS)

        if not selected_agent_name or selected_agent_name not in AGENTS:
            return {
                "error": "Could not determine appropriate agent.",
                "input": task_input
            }

        selected_agent = AGENTS[selected_agent_name]
        print(f"[Orchestrator] Routing to agent: {selected_agent_name}")

        # # 🛠️ Flexible run handling
        # # Use:
        # if isinstance(user_input, str):
        #     input_data = {"resume_text": user_input}
        # else:
        #     input_data = user_input
        # if isinstance(selected_agent, dict):
        #     run_fn = selected_agent.get("run")
        # elif hasattr(selected_agent, "run"):
        #     run_fn = selected_agent.run
        # else:
        #     return {"error": "Agent does not have a callable 'run' method."}

        # if not callable(run_fn):
        #     return {"error": "'run' is not callable."}

        # output = run_fn(input_data)
        print("sending for adapted output")
        print(selected_agent)
        print(selected_agent_name)

        adapted_input = adapt_input_to_agent(selected_agent_name, user_input)
        # print(adapted_input)
        response = selected_agent.run(adapted_input)
        # ... existing logic to get the response ...

        # --- ADD THIS MEMORY LOGIC ---
        # Save the final interaction to the shared memory
        shared_memory.store("last_input", user_input)
        # Convert dicts to a string for consistent storage
        response_str = json.dumps(response) if isinstance(response, dict) else str(response)
        shared_memory.store("last_response", response_str)
        # --- END OF MEMORY LOGIC ---

        return response
    except Exception as e:
        return {"error": str(e)}



# if __name__ == "__main__":
#     query = "Can you help me write a professional resume for a data scientist?"
#     response = handle_user_input(query)
#     print(json.dumps(response, indent=2))




# graph TD
#     UserInput[User Input]
#     Orchestrator[🤖 Orchestrator Agent]
#     Router[LLM-based Router]
#     Registry[Agent Manifest]
#     Agent[ToolAgent/LlmAgent]
#     Output[Output to User]

#     UserInput --> Orchestrator
#     Orchestrator --> Router
#     Router --> Registry
#     Registry --> Agent
#     Agent --> Orchestrator
#     Orchestrator --> Output
