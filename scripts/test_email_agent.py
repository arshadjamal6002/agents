import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from agents.email_agent.prompt import build_email_prompt
from agents.email_agent.tool import tool

# prompt = build_email_prompt(
#     purpose="apply for a software engineering internship",
#     content="I have strong Python and ML skills, graduated recently. I want to express interest.",
#     tone="professional"
# )

# print(prompt)


# ###############################################
# result = tool({
#     "purpose": "follow up after an interview",
#     "content": "I want to thank them and express strong interest in the role",
#     "tone": "polite"
# })

# print("✉️ Subject:", result["subject"])
# print("\n📨 Body:\n", result["body"])

# ##################################################

from agents.email_agent.tool import tool

sample_input = {
    "purpose": "thank the interviewer and express interest",
    "content": "Had a great discussion on LLMs. Mention the role of Data Scientist.",
    "tone": "enthusiastic"
}

print(tool(sample_input))

#####################################################

