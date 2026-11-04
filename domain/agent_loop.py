from domain.ports.llm_port import LLMPort
from domain.ports.memory_port import MemoryPort
from domain.ports.tool_port import ToolPort
from domain.ports.storage_port import StoragePort
from domain.models import AgentState,AgentStep,ToolCall
import json






SYSTEM_PROMPT = "You are an intelligent agent that can perform tasks and answer questions. You have access to a set of tools that you can use to help you accomplish your goals. You should think carefully about which tool to use and how to use it. You should also remember relevant information from previous interactions."
class AgentLoop:
    def __init__(
        self,
        llm: LLMPort,
        memory: MemoryPort,
        tools: ToolPort,
        storage: StoragePort,
        max_steps: int = 5
    ):
        self.llm = llm
        self.memory = memory
        self.tools = tools
        self.storage = storage
        self.max_steps = max_steps
    
    def run(self, user_input: str, session_id: str = "default") -> AgentState:
        # misma lógica del Proyecto 1
        # pero en vez de ollama.chat → self.llm.invoke()
        if self.max_steps <= 0:
            raise ValueError("max_steps must be greater than 0")
       
        state = AgentState(input=user_input)
        if len(self.memory.get_messages()) == 0:
            self.memory.add_message("system", SYSTEM_PROMPT)
            # Usamos el puerto de storage para buscar recuerdos
            memories = self.storage.retrieve(query=user_input, top_k=3)
            if memories:
                memory_text = "\n".join(f"- {m}" for m in memories)
                self.memory.add_message("system", f"Relevant memories:\n{memory_text}")

        self.memory.add_message("user", user_input)
        while not state.is_final and len(state.steps) < self.max_steps:
            # Obtenemos el historial desde el puerto de memoria
            messages = self.memory.get_messages()
            
            # LLAMADA AL LLM A TRAVÉS DEL PUERTO
            llm_text = self.llm.invoke(messages)
            
            # Parseamos la respuesta (esta función es pura, va en domain/utils.py)
            step = parse_llm_response(llm_text)
            
            if step.is_final:
                state.is_final = True
                state.final_answer = step.observation
            else:
                tool_name = step.action.tool_name
                
                # EJECUCIÓN DE HERRAMIENTAS A TRAVÉS DEL PUERTO
                try:
                    # El puerto ToolPort se encarga del harness y permisos internamente
                    step.observation = self.tools.execute(
                        tool_name=tool_name, 
                        tool_input=step.action.input
                    )
                except Exception as e:
                    step.observation = f"Error ejecutando la herramienta '{tool_name}': {str(e)}"
                
                # Guardamos en memoria el pensamiento del agente y el resultado de la tool
                self.memory.add_message("assistant", llm_text)
                self.memory.add_message("user", f"Observation: {step.observation}")
            
            state.steps.append(step)

        # 4. Cierre y guardado en Largo Plazo
        if not state.is_final:
            state.final_answer = "No se puede completar la tarea en el número máximo de pasos."
            
        # GUARDADO EN STORAGE A TRAVÉS DEL PUERTO
        self.storage.store(
            session_id=session_id,
            content=f"User asked: {user_input}. Agent answered: {state.final_answer}"
        )
        
        return state
        
      


def parse_llm_response(text: str) -> AgentStep:
    lines = text.strip().split("\n")
    
    
    
    # Caso 1: tiene Final Answer
    if "Final Answer:" in text:
        thought = ""
        final_answer = ""
        for line in lines:
            if line.startswith("Thought:"):
                thought = line.replace("Thought:", "").strip()
            if line.startswith("Final Answer:"):
                final_answer = line.replace("Final Answer:", "").strip()
        return AgentStep(
            thought=thought,
            observation=final_answer,
            is_final=True
        )
    
    # Caso 2: tiene Action
    thought = ""
    tool_name = ""
    tool_input = {}
    for line in lines:
        
        
        if line.startswith("Thought:"):
            thought = line.replace("Thought:", "").strip()
        if line.startswith("Action:"):
            tool_name = line.replace("Action:", "").strip()
        if line.startswith("Action Input:"):
            raw = line.replace("Action Input:", "").strip()
            try:
                tool_input=json.loads(raw)
            except:
                tool_input={}# convierte string a dict
    
    return AgentStep(
        thought=thought,
        action=ToolCall(tool_name=tool_name, input=tool_input),
        is_final=False
    )