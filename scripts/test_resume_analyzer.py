from agents.resume_analyzer_agent.prompt import build_resume_prompt

# prompt = build_resume_prompt(
#     resume="Arshad Jamal, B.Tech CSE, interned at TCS, skills: Python, Excel, SQL",
#     job_description="Looking for a Data Analyst with Python, Tableau, and ML experience."
# )

# print(prompt)


####################################################

sample = {
    "resume_text": "Arshad Jamal, B.Tech CSE, interned at TCS, skilled in Python, SQL, Excel",
    "job_description": "Hiring a data analyst skilled in Python, Tableau, and machine learning."
}

from agents.resume_analyzer_agent.tool import tool
print(tool(sample))


#######################################################

