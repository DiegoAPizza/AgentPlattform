
from abc import ABC, abstractmethod

class StoragePort(ABC):
    @abstractmethod
    def store(self, session_id:str,content:str) -> None:
        pass
    @abstractmethod
    
    def retrieve(self, query: str, top_k: int) -> list[str]:
        pass