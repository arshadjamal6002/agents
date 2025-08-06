# utils/router.py

import json
from typing import List, Dict
from langchain_openai import OpenAI
import os 
from dotenv import load_dotenv
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

def build_router_prompt(user_input: str, agents: List[Dict]) -> str:
    """
    Constructs a routing prompt with agent descriptions.
    """
    agent_descriptions = "\n".join([
        f"- {agent['name']}: {agent.get('description', 'No description provided')}"
        for agent in agents
    ])

    prompt = f"""
You are a task router in a multi-agent AI system.

Below are the available agents and their functions:
{agent_descriptions}

Given the following user query:
"{user_input}"

Decide which ONE agent is most appropriate to handle this query.

Respond with only a JSON object like:
{{ "selected_agent": "agent_name_here" }}
"""
    return prompt.strip()

def choose_agent(user_input: str, agents: List[Dict]) -> str:
    """
    Routes user input to the best matching agent.
    """
    prompt = build_router_prompt(user_input, agents)
    llm = OpenAI(openai_api_key=openai_key, model_name="gpt-3.5-turbo-instruct", temperature=0)
    result = llm.invoke(prompt).strip()

    try:
        response = json.loads(result)
        return response.get("selected_agent", "")
    except Exception:
        return ""

