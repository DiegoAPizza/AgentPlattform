
import asyncio
import logging
import json
from concurrent.futures import ThreadPoolExecutor
from domain.agent_loop import AgentLoop,AgentState
from domain.ports.llm_port import LLMPort

logger = logging.getLogger("agentcore.shadow")
executor = ThreadPoolExecutor(max_workers=2)

class ShadowRunner:
    def __init__(self, v1_llm: LLMPort, v2_llm: LLMPort):
        self.v1_llm = v1_llm
        self.v2_llm = v2_llm
    
    def run(
        self,
        user_input: str,
        session_id: str,
        memory_factory,  # función que crea un MemoryPort nuevo
        tools,
        storage
    ) -> AgentState:
        # 1. Correr v1 — respuesta real al usuario
        agent_v1 = AgentLoop(
            llm=self.v1_llm,
            memory=memory_factory(f"{session_id}-v1"),
            tools=tools,
            storage=storage
        )
        result_v1 = agent_v1.run(user_input, session_id=session_id)
        
        # 2. Correr v2 en background — sin bloquear
        executor.submit(
            self._run_shadow,
            user_input,
            session_id,
            memory_factory,
            tools,
            storage,
            result_v1.final_answer
        )
        
        # 3. Retornar v1 inmediatamente
        return result_v1
    def _run_shadow(
        self,
        user_input,
        session_id,
        memory_factory,
        tools,
        storage,
        v1_answer
    ):
        try:
            agent_v2 = AgentLoop(
                llm=self.v2_llm,
                memory=memory_factory(f"{session_id}-v2"),
                tools=tools,
                storage=storage
            )
            result_v2 = agent_v2.run(user_input, session_id=f"{session_id}-shadow")
            
            # Loguear comparación para análisis posterior
            logger.info(json.dumps({
                "event": "shadow_comparison",
                "session_id": session_id,
                "input": user_input,
                "v1_answer": v1_answer,
                "v2_answer": result_v2.final_answer
            }))
        except Exception as e:
            logger.error(f"Shadow run failed: {e}")