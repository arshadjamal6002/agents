# agents/sql_generator_agent/tool.py

from typing import Dict
from langchain_openai import OpenAI
from agents.sql_generator_agent.prompt import build_sql_prompt
import os 
from dotenv import load_dotenv
load_dotenv()

def tool(input: Dict[str, str]) -> Dict[str, str]:
    """
    Generates a SQL query from natural language.

    Input:
        {
            "instruction": "Get top 5 customers by revenue",
            "table_schema": "customers(id, name, revenue)",
            "dialect": "PostgreSQL"
        }

    Output:
        {
            "sql": "SELECT ...;"
        }
    """
    try:
        instruction = input.get("instruction")
        table_schema = input.get("table_schema", "")
        dialect = input.get("dialect", "PostgreSQL")

        if not instruction:
            return {"error": "Missing 'instruction' input."}

        prompt = build_sql_prompt(instruction, table_schema, dialect)

        llm = OpenAI(temperature=0.2, model_name="gpt-3.5-turbo-instruct")
        raw_sql = llm.invoke(prompt).strip()

        # Clean result (remove backticks, comments, explanations if needed)
        sql = raw_sql.split(";")[0].strip() + ";" if ";" not in raw_sql else raw_sql.strip()

        return {"sql": sql}

    except Exception as e:
        return {"error": str(e)}
