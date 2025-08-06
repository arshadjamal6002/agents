# agents/code_explainer_agent/prompt.py

PROMPT_TEMPLATE = """
You are an expert software engineer.

Explain the following code in {language} at a {depth} level of detail.

Code:


Your output must follow this format:

1. 📌 **High-Level Summary**
2. 🔍 **Line-by-Line Explanation**
3. ✅ **Possible Improvements or Best Practices**

Only output the explanation. Don't restate the code.
"""

def build_explanation_prompt(code: str, language: str = "Python", depth: str = "detailed") -> str:
    return PROMPT_TEMPLATE.format(
        code=code.strip(),
        language=language.strip(),
        depth=depth.strip()
    )