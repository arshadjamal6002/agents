# agents/code_explainer_agent/agent.py
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from adk.agents import ToolAgent
from .tool import tool

agent = ToolAgent(
    name="code_explainer_agent",
    description="Explains code step-by-step with summaries and recommendations.",
    tool=tool
)


# agent = {
#     "name": "code_explainer_agent",
#     "description": "Explains code step-by-step with summaries and recommendations.",
#     "run": tool  # main function the orchestrator will call
# }