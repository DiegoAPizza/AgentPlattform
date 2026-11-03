# api/routes/agent.py
def chat(request: ChatRequest):
    # instancia adaptadores
    llm = OllamaAdapter()
    memory = RedisAdapter(session_id=request.session_id)
    
    # inyecta al dominio
    agent = AgentLoop(llm=llm, memory=memory)
    
    # el dominio nunca supo qué adaptador era
    result = agent.run(request.message)