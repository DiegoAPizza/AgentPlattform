from domain.ports.llm_port import LLMPort
import ollama

class OllamaAdapter(LLMPort):
    def __init__(self, model: str = "llama3.2"):
        self.model = model
    
    def invoke(self, messages: list[dict]) -> str:
        response = ollama.chat(model=self.model, messages=messages)
        return response["message"]["content"]