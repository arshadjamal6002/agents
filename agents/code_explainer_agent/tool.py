# agents/code_explainer_agent/tool.py

from typing import Dict
from langchain_openai import OpenAI
from agents.code_explainer_agent.prompt import build_explanation_prompt
import os 
from dotenv import load_dotenv
load_dotenv()

def tool(input: Dict[str, str]) -> Dict[str, str]:
    """
    Explains code with structured reasoning.

    Input:
        {
            "code": "<code snippet>",
            "language": "Python",
            "depth": "step-by-step"
        }

    Output:
        {
            "summary": "...",
            "line_by_line": "...",
            "recommendations": "..."
        }
    """
    try:
        code = input.get("code")
        language = input.get("language", "Python")
        depth = input.get("depth", "detailed")

        if not code:
            return {"error": "Missing 'code' input."}

        prompt = build_explanation_prompt(code, language, depth)

        llm = OpenAI(temperature=0.3, model_name="gpt-3.5-turbo-instruct")
        output = llm.invoke(prompt)

        # Parse into 3 sections (based on numbered structure)
        sections = output.split("2. 🔍 **Line-by-Line Explanation**")
        summary = sections[0].split("1. 📌 **High-Level Summary**")[-1].strip() if len(sections) > 1 else ""
        rest = sections[1].split("3. ✅ **Possible Improvements or Best Practices**") if len(sections) > 1 else ["", ""]
        line_by_line = rest[0].strip()
        recommendations = rest[1].strip() if len(rest) > 1 else ""

        return {
            "summary": summary,
            "line_by_line": line_by_line,
            "recommendations": recommendations
        }

    except Exception as e:
        return {"error": str(e)}
