# agents/doc_qa_agent/agent.
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from adk.agents import ToolAgent
from .tool import tool


# agent = {
#     "name": "doc_qa_agent",
#     "description": "Answers questions from PDF documents.",
#     "run": tool  # main function the orchestrator will call
# }

agent = ToolAgent(
    name="doc_qa_agent",
    description="Answers questions from PDF documents.",
    tool=tool
)