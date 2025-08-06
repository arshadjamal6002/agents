# agents/resume_analyzer_agent/agent.py
import sys
import os
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from adk.agents import ToolAgent
from .tool import tool

agent = ToolAgent(
    name="resume_analyzer_agent",
    description="Analyzes resumes and gives suggestions based on job description.",
    tool=tool
)

# agent = {
#     "name": "resume_analyzer_agent",
#     "description": "Analyzes resumes and gives suggestions based on job description.",
#     "run": tool  # main function the orchestrator will call
# }

