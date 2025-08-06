# agents/sql_generator_agent/prompt.py

PROMPT_TEMPLATE = """
You are a senior data engineer skilled in SQL.

Generate a SQL query based on the user's request.

Instruction:
{instruction}

Table Schema:
{table_schema}

SQL Dialect: {dialect}

Only return valid SQL. Do not include any explanation or formatting.
"""

def build_sql_prompt(instruction: str, table_schema: str = "", dialect: str = "PostgreSQL") -> str:
    return PROMPT_TEMPLATE.format(
        instruction=instruction.strip(),
        table_schema=table_schema.strip() or "Not provided",
        dialect=dialect.strip() or "PostgreSQL"
    )
