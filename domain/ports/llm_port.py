
from abc import ABC, abstractmethod

class LLMPort(ABC):
    @abstractmethod
    def invoke(self, messages: list[dict]) -> str:
        pass