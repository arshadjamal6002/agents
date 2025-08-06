# agents/email_agent/agent.py
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from adk.agents import ToolAgent
from .tool import tool

agent = ToolAgent(
    name="email_generator_agent",
    description="Generates emails from purpose, content, and tone.",
    tool=tool
)


# agent = {
#     "name": "email_generator_agent",
#     "description": "Generates emails from purpose, content, and tone.",
#     "run": tool  # main function the orchestrator will call
# }