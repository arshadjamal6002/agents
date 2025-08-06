# from config.agents_manifest import agents  # load this JSON manually

# NEW (correct)
import json
import os

# Build the path to the JSON file
manifest_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'agents_manifest.json')

# Load the JSON file
with open(manifest_path, 'r') as f:
    agents = json.load(f)

from utils.router import choose_agent
user_input = "Can you create slides about generative AI?"

selected = choose_agent(user_input, agents)
print(f"Selected agent: {selected}")
