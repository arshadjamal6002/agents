# agents/email_agent/prompt.py

EMAIL_PROMPT_TEMPLATE = """
You are an expert assistant that writes well-crafted, human-like emails.

Write an email with the following context:
- Purpose: {purpose}
- Tone: {tone}
- Content Brief: {content}

Return the output in this format:

Subject: <short subject line>
Body:
<email body>
"""

def build_email_prompt(purpose: str, content: str, tone: str = "formal") -> str:
    return EMAIL_PROMPT_TEMPLATE.format(
        purpose=purpose.strip(),
        tone=tone.strip(),
        content=content.strip()
    )
