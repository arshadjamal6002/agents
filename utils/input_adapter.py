import os
import logging
import json

def load_agent_manifest(agent_name):
    print(f"Loading manifest for agent: {agent_name}")
    path = os.path.join("agents", agent_name, "config.json")
    abs_path = os.path.abspath(path)
    
    logging.info(f"Looking for config at: {abs_path}")
    
    if not os.path.exists(abs_path):
        logging.warning(f"No config.json found for agent '{agent_name}'")
        return {}

    with open(abs_path, "r") as f:
        return json.load(f)


def adapt_input_to_agent(agent_name, user_query):
    """
    Transforms raw user input (string or dict) into the format expected by the agent,
    based on its declared 'required_inputs' in config.json.
    """
    manifest = load_agent_manifest(agent_name)
    required_fields = manifest.get("required_inputs", [])

    if not required_fields:
        return user_query

    # --- START: THE FIX ---
    # If the input from the test is a dictionary, map its values correctly.
    if isinstance(user_query, dict):
        adapted = {field: user_query.get(field) for field in required_fields}
        logging.debug(f"Adapted input for {agent_name}: {adapted}")
        return adapted
    # --- END: THE FIX ---

    # Fallback logic for when user_query is a simple string.
    if len(required_fields) == 1:
        return {required_fields[0]: user_query}
    
    # Default fallback: use the string query for all fields
    adapted = {field: user_query for field in required_fields}
    logging.debug(f"Adapted input for {agent_name} (fallback): {adapted}")
    return adapted