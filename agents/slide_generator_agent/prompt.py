# agents/slide_generator_agent/prompt.py

PROMPT_TEMPLATE_TOPIC = """
You are a presentation design assistant.

Create a slide deck based on the topic: "{topic}"

Each slide should include:
- Slide title
- 2–4 concise bullet points

Output must be valid JSON like this:
{{
  "slides": [
    {{"title": "...", "bullets": ["...", "..."]}},
    ...
  ]
}}
"""

PROMPT_TEMPLATE_BULLETS = """
You are a presentation design assistant.

Using the following bullet points, organize them into slides.

Bullets:
{bullets}

Each slide must include:
- Slide title
- 2–4 concise bullet points

Output format:
{{
  "slides": [
    {{"title": "...", "bullets": ["...", "..."]}},
    ...
  ]
}}
"""

def build_slide_prompt(topic: str = "", bullets: list = None) -> str:
    if bullets:
        return PROMPT_TEMPLATE_BULLETS.format(
            bullets="\n".join(f"- {b}" for b in bullets)
        )
    else:
        return PROMPT_TEMPLATE_TOPIC.format(topic=topic.strip())
