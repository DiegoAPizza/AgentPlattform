 
from abc import ABC, abstractmethod

class ToolPort(ABC):
    @abstractmethod
    def execute(self,tool_name: str,tool_input:dict) -> str:
        pass
    @abstractmethod

    def list_tools(self) -> list[dict]:
        pass