
from typing import List
from domain.ports.memory_port import MemoryPort

class InMemoryMemoryAdapter(MemoryPort):
    def __init__(self, max_messages: int = 20):
        # Usamos "messages" (plural) para la lista
        self.messages = []
        # Usamos "max_messages" (plural)
        self.max_messages = max_messages

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    # ¡ACÁ ESTABA EL ERROR! Lo cambiamos a plural
    def get_messages(self) -> list[dict]:  
        return self.messages

    def clear(self) -> None:
        self.messages = []