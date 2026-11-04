import pytest
from domain.agent_loop import AgentLoop

# --- Mocks rápidos ---
class MockLLMAdapter:
    def __init__(self, responses: list[str]):
        self.responses = responses
        self.call_count = 0

    def invoke(self, messages: list[dict]) -> str:
        response = self.responses[self.call_count]
        self.call_count += 1
        return response

class MockMemoryAdapter:
    def __init__(self):
        self.messages = []
    def add_message(self, role, content): self.messages.append({"role": role, "content": content})
    def get_messages(self): return self.messages
    def clear(self): self.messages = []

class MockToolAdapter:
    def execute(self, tool_name: str, tool_input: dict) -> str:
        return f"Tool {tool_name} executed with {tool_input}"
    def list_tools(self): return ["calculator"]

class MockStorageAdapter:
    def store(self, session_id: str, content: str): pass
    def retrieve(self, query: str, top_k: int): return []

# --- Test 1 ---
def test_agent_loop_final_answer_directo():
    mock_llm = MockLLMAdapter(responses=["Thought: Ya sé la respuesta.\nFinal Answer: Hola, soy un agente."])
    agent = AgentLoop(llm=mock_llm, memory=MockMemoryAdapter(), tools=MockToolAdapter(), storage=MockStorageAdapter())

    state = agent.run("Hola, ¿cómo estás?")

    assert state.is_final is True
    assert state.final_answer == "Hola, soy un agente."
    assert len(state.steps) == 1

# --- Test 2 ---
def test_agent_loop_usa_herramienta():
    llm_responses = [
        "Thought: Necesito calcular 2+2.\nAction: calculator\nAction Input: {\"expr\": \"2+2\"}",
        "Thought: Ya tengo el resultado.\nFinal Answer: El resultado es 4."
    ]
    mock_llm = MockLLMAdapter(responses=llm_responses)
    mock_memory = MockMemoryAdapter()
    
    agent = AgentLoop(llm=mock_llm, memory=mock_memory, tools=MockToolAdapter(), storage=MockStorageAdapter())

    state = agent.run("Cuánto es 2+2?")

    assert state.is_final is True
    assert state.final_answer == "El resultado es 4."
    assert len(state.steps) == 2 
    assert state.steps[0].action.tool_name == "calculator"
    observation_messages = [m for m in mock_memory.messages if "Observation:" in m["content"]]
    assert any("Tool calculator executed" in m["content"] for m in observation_messages)