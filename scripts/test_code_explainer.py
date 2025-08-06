from agents.code_explainer_agent.prompt import build_explanation_prompt
from agents.code_explainer_agent.tool import tool

# code = "def factorial(n): return 1 if n == 0 else n * factorial(n-1)"
# prompt = build_explanation_prompt(code, language="Python", depth="step-by-step")
# print(prompt)

# ########################################

# sample_input = {
#     "code": "def add(a, b): return a + b",
#     "language": "Python",
#     "depth": "basic"
# }

# result = tool(sample_input)
# print("🧠 Summary:\n", result["summary"])
# print("\n🪄 Line-by-Line:\n", result["line_by_line"])
# print("\n✅ Recommendations:\n", result["recommendations"])


# ############################################

from agents.code_explainer_agent.tool import tool

test_code = {
    "code": "def reverse_list(lst): return lst[::-1]",
    "language": "Python",
    "depth": "detailed"
}

response = tool(test_code)

print("🔹 Summary:\n", response["summary"])
print("🔸 Line-by-Line:\n", response["line_by_line"])
print("✅ Recommendations:\n", response["recommendations"])
