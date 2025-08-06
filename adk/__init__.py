# makes this a package
class LlmAgent:
    """A base class for agents that primarily use an LLM for complex, non-tool-based tasks."""
    def run(self, input: dict) -> dict:
        # This base method is designed to be overridden by child agents like WorkflowAgent.
        raise NotImplementedError("Each LlmAgent must implement its own run method.")