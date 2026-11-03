import redis
import json
from typing import List
from domain.ports.memory_port import MemoryPort

class RedisMemoryAdapter(MemoryPort):
    def __init__(
        self, 
        session_id: str, 
        max_messages: int = 20, 
        ttl: int = 3600,
        host: str = "localhost", 
        port: int = 6379
    ):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)
        self.key = f"session:{session_id}:messages"
        self.max_messages = max_messages
        self.ttl = ttl
    
    def add_message(self, role: str, content: str) -> None:
        message = {"role": role, "content": content}
        message_json = json.dumps(message)
        
        # Uso de Pipeline para eficiencia (1 solo viaje a Redis en vez de 3)
        pipe = self.client.pipeline()
        pipe.rpush(self.key, message_json)
        pipe.ltrim(self.key, -self.max_messages, -1)
        pipe.expire(self.key, self.ttl)
        pipe.execute()
        
    def get_messages(self) -> List[dict]:
        raw_messages = self.client.lrange(self.key, 0, -1)
        return [json.loads(msg) for msg in raw_messages]
    
    def clear(self) -> None:
        self.client.delete(self.key)