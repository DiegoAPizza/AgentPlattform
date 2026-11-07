from domain.ports.storage_port import StoragePort

class MockStorageAdapter(StoragePort):
    def __init__(self):
        # Usamos una lista simple en memoria para simular la base de datos
        self._storage = []

    def store(self, session_id: str, content: str) -> None:
        # Guardamos el string junto con su session_id
        self._storage.append({"session_id": session_id, "content": content})

    def retrieve(self, query: str, top_k: int) -> list[str]:
        # Simulamos una búsqueda vectorial devolviendo "recuerdos" falsos
        # Para hacerlo más realista, devolvemos cosas que tengan que ver con la query
        if not self._storage:
            return []
        
        # Devolvemos los últimos "top_k" recuerdos guardados
        return [item["content"] for item in self._storage[-top_k:]]