import pybreaker
import logging
from adapters.llm.ollama_adapter import OllamaAdapter
from domain.ports.llm_port import LLMPort

logger = logging.getLogger("agentcore.circuit_breaker")

class _BreakerListener(pybreaker.CircuitBreakerListener):
    def state_change(self, cb, old_state, new_state):
        logger.warning(f"Circuit breaker: {old_state} → {new_state}")
# El circuit breaker abre después de 3 fallos consecutivos
# y espera 30 segundos antes de intentar de nuevo
breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=30,
    listeners=[_BreakerListener()]
)


class ResilientOllamaAdapter(LLMPort):
    def __init__(self, model: str = "llama3.2"):
        self._adapter = OllamaAdapter(model=model)
    
    
    def invoke(self, messages: list[dict]) -> str:
     
        try:
            return breaker.call(self._adapter.invoke, messages)
        except pybreaker.CircuitBreakerError:
            logger.error("Circuit breaker OPEN — LLM unavailable")
            return "Final Answer: El servicio no está disponible temporalmente."