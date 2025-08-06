# agents/resume_analyzer_agent/tool.py

import logging
from typing import Dict, Union
from langchain_openai import OpenAI
from agents.resume_analyzer_agent.prompt import build_resume_prompt
import json
import os 
from dotenv import load_dotenv
load_dotenv()

# Setup logging
# Configure the default logging level to be less noisy (e.g., INFO or WARNING)
logging.basicConfig(level=logging.INFO)
# Get the logger for this specific file
logger = logging.getLogger(__name__)
# Set ONLY this logger to output detailed DEBUG messages
logger.setLevel(logging.DEBUG)

openai_api_key = os.getenv("OPENAI_API_KEY")

def tool(input: Dict[str, str]) -> Union[Dict, str]:
    """
    Analyzes a resume against a job description using LLM.
    """
    logger.debug("Received input: %s", input)

    try:
        resume = input.get("resume_text", "")
        job_description = input.get("job_description", "")

        if not resume or not job_description:
            logger.warning("Missing input fields.")
            return {"error": "Missing required input: resume_text or job_description"}

        prompt = build_resume_prompt(resume, job_description)
        # logger.debug("Built prompt: %s", prompt)

        llm = OpenAI(
            openai_api_key=openai_api_key,
            temperature=0.3,
            model_name="gpt-3.5-turbo-instruct"
        )

        result = llm.invoke(prompt).strip()
        # logger.debug("LLM raw result: %s", result)

        try:
            parsed = json.loads(result)
            # logger.debug("Parsed LLM result: %s", parsed)
            return parsed
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON from LLM result")
            return {
                "error": "LLM returned invalid JSON",
                "raw_output": result
            }

    except Exception as e:
        logger.exception("Unexpected error occurred in resume analyzer tool")
        return {"error": str(e)}
