# agents/email_agent/tool.py

from typing import Dict
from openai import OpenAIError
from langchain_openai import OpenAI
from agents.email_agent.prompt import build_email_prompt
from dotenv import load_dotenv
load_dotenv()

def tool(input: Dict[str, str]) -> Dict[str, str]:
    """
    Generates an email given purpose, content brief, and tone.
    
    Input:
        {
            "purpose": "follow up after interview",
            "content": "mention excitement about the company",
            "tone": "professional"
        }
    
    Output:
        {
            "subject": "...",
            "body": "..."
        }
    """
    try:
        purpose = input.get("purpose", "")
        content = input.get("content", "")
        tone = input.get("tone", "formal")

        if not purpose or not content:
            return {"error": "Missing required fields: purpose or content."}

        prompt = build_email_prompt(purpose, content, tone)

        llm = OpenAI(temperature=0.3, model_name="gpt-3.5-turbo-instruct")
        response = llm.invoke(prompt)

        # Simple parsing (could improve later)
        if "Subject:" in response and "Body:" in response:
            subject = response.split("Subject:")[1].split("Body:")[0].strip()
            body = response.split("Body:")[1].strip()
        else:
            subject = "Generated Email"
            body = response.strip()

        return {
            "subject": subject,
            "body": body
        }

    except OpenAIError as e:
        return {"error": f"OpenAI API error: {e}"}
    except Exception as e:
        return {"error": str(e)}
