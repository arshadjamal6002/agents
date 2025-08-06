# agents/resume_analyzer_agent/prompt.py

PROMPT_TEMPLATE = """
You are an expert career advisor and resume reviewer.

Analyze the resume and job description below.

Resume:
{resume}

Job Description:
{job_description}

---

Return a JSON object with:
1. "match_score": score from 0 to 100 based on how well resume fits job
2. "summary": extracted summary with keys - skills, experience, education
3. "suggestions": list of 2-5 suggestions to improve the resume

Only return a valid JSON object. Do not explain anything.
"""

def build_resume_prompt(resume: str, job_description: str) -> str:
    return PROMPT_TEMPLATE.format(
        resume=resume.strip(),
        job_description=job_description.strip()
    )
