# agents/sql_generator_agent/agent.py
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from adk.agents import ToolAgent
from .tool import tool

agent = ToolAgent(
    name="sql_generator_agent",
    description="Generates SQL queries from plain English instructions.",
    tool=tool
)


# agent = {
#     "name": "sql_generator_agent",
#     "description": "Generates SQL queries from plain English instructions.",
#     "run": tool  # main function the orchestrator will call
# }