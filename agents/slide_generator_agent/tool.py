# agents/slide_generator_agent/tool.py

from typing import Dict, Union
from langchain_openai import OpenAI
from agents.slide_generator_agent.prompt import build_slide_prompt
import json
import os 
import re
from dotenv import load_dotenv
load_dotenv()

def tool(input: Dict[str, Union[str, list]]) -> Union[Dict, str]:
    """
    Generates a slide deck from a topic or bullet points.

    Input:
        { "topic": "...", OR "bullets": ["...", "..."] }

    Output:
        {
            "slides": [
                {
                    "title": "...",
                    "bullets": ["...", "..."]
                },
                ...
            ]
        }
    """
    try:
        topic = input.get("topic", "").strip()
        bullets = input.get("bullets", [])

        if not topic and not bullets:
            return {"error": "Provide either a 'topic' or a list of 'bullets'."}

        prompt = build_slide_prompt(topic=topic, bullets=bullets)

        llm = OpenAI(temperature=0.4, model_name="gpt-3.5-turbo-instruct")
        result = llm.invoke(prompt).strip()

        try:
            # Clean up the JSON by removing trailing commas before parsing
            clean_result = re.sub(r',\s*([\]}])', r'\1', result)
            parsed = json.loads(clean_result)
            return parsed
        except json.JSONDecodeError:
            return {
                "error": "LLM returned invalid JSON",
                "raw_output": result
            }

    except Exception as e:
        return {"error": str(e)}
