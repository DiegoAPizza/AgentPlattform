from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from api.schemas.schema import ChatRequest, ChatResponse # Asegurate que esta ruta sea la correcta
from core.shawdow_mode import ShadowRunner
from adapters.llm.mock_adapter import MockLLMAdapter
from adapters.memory.in_memory_adapter import InMemoryMemoryAdapter # <-- Usamos RAM en vez de Redis
from adapters.tools.mockadapter import MockToolAdapter
from adapters.storage.mock_adapter_storage import MockStorageAdapter
import time
from core.quality_monitor import QualityMonitor

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()
monitor= QualityMonitor()
@router.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat(request: Request, body: ChatRequest):
    start = time.time()
    # 1. Configuramos los dos LLMs (el actual y el nuevo prompt)
    v1_llm = MockLLMAdapter("Thought: v1.\nFinal Answer: Respuesta del Agente en Producción (V1)")
    v2_llm = MockLLMAdapter("Thought: v2.\nFinal Answer: Respuesta del Agente Nuevo (V2)")
    
    # 2. Instanciamos el Runner
    runner = ShadowRunner(v1_llm=v1_llm, v2_llm=v2_llm)
    
    # 3. Ejecutamos
    answer = runner.run(
        user_input=body.message,
        session_id=body.session_id,
        memory_factory=lambda sid: InMemoryMemoryAdapter(), # El factory ahora crea memorias en RAM
        tools=MockToolAdapter(),
        storage=MockStorageAdapter()
    )
   
    monitor.record(answer, elapsed_seconds=time.time() - start)
    return ChatResponse(response=answer.final_answer)