from domain.ports.llm_port import LLMPort

class MockLLMAdapter(LLMPort):
    def __init__(self, predefined_response: str = "Respuesta simulada del LLM"):
        # Acá guardamos lo que queremos que devuelva
        self.predefined_response = predefined_response
        # Guardamos los mensajes que recibió para poder auditarlos en el test
        self.received_messages = []

    def invoke(self, messages: list[dict]) -> str:
        self.received_messages.append(messages)  # ← agregar esto
        return self.predefined_response