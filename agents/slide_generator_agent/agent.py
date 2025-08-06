# agents/slide_generator_agent/agent.py
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from adk.agents import ToolAgent
from .tool import tool

agent = ToolAgent(
    name="slide_generator_agent",
    description="Generates structured slide content from a topic or bullet list.",
    tool=tool
)


# agent = {
#     "name": "slide_generator_agent",
#     "description": "Generates structured slide content from a topic or bullet list.",
#     "run": tool  # main function the orchestrator will call
# }