from agents.slide_generator_agent.prompt import build_slide_prompt

# print(build_slide_prompt(topic="Introduction to Generative AI"))
# print(build_slide_prompt(bullets=[
#     "Benefits of using open-source tools",
#     "Best practices for reproducibility",
#     "ML model versioning with DVC",
#     "CI/CD pipelines for ML"
# ]))


###############################################

sample_input = {"topic": "Introduction to GenAI"}
from agents.slide_generator_agent.tool import tool
print(tool(sample_input))




####################################################


