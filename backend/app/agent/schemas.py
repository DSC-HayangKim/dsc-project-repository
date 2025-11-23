from pydantic import BaseModel

class AgentRequest(BaseModel):
    query: str
    llm_type: str = "openai"  # "openai" or "ollama"

class AgentResponse(BaseModel):
    response: str
