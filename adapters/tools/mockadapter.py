from domain.ports.tool_port import ToolPort

class MockToolAdapter(ToolPort):
    def execute(self, tool_name: str, tool_input: dict) -> str:
        # Simulamos que la herramienta se ejecutó correctamente
        return f"Herramienta '{tool_name}' ejecutada con éxito. Input: {tool_input}"

    def list_tools(self) -> list[str]:
        # Devolvemos una lista falsa de herramientas disponibles
        return ["calculator", "get_date", "search"]