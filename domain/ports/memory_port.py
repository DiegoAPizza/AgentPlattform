
from abc import ABC, abstractmethod

class MemoryPort(ABC):
    @abstractmethod
    def get_message(self) -> list[dict]:
        pass
    @abstractmethod
    
    def add_message(self, role: str, content: str) -> None:        pass
    @abstractmethod
        
    def clear(self) -> None:
        pass