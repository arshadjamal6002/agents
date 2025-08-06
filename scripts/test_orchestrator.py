from orchestrator_agent import handle_user_input
import json


query = "Can you help me write a professional resume for a data scientist?"
response = handle_user_input(query)
print(json.dumps(response, indent=2))