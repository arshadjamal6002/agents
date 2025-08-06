# adk/agents/base.py

from typing import Callable

class ToolAgent:
    def __init__(self, name: str, description: str, tool: Callable):
        self.name = name
        self.description = description
        self.tool = tool  # this is a callable utility function

    def run(self, input_data: dict) -> dict:
        return self.tool(input_data)


class LlmAgent:
    def __init__(self, name: str, description: str, prompt_template: str, model: Callable):
        self.name = name
        self.description = description
        self.prompt_template = prompt_template
        self.model = model

    def run(self, input_data: dict) -> dict:
        prompt = self.prompt_template.format(**input_data)
        output = self.model(prompt)
        return {"output": output}
