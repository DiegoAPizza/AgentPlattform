
from typing import List
from domain.ports.memory_port import MemoryPort

class InMemoryAdapter(MemoryPort):
    def __init__(
        self
    ):
        self.list= []
    
    def add_message(self, role: str, content: str) -> None:
        self.list.append({"role": role, "content": content})
        
    def get_messages(self) -> List[dict]:
        return self.list
    
    def clear(self) -> None:
        self.list.clear()