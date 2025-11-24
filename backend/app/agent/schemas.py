from typing import List, Tuple, Optional
from pydantic import BaseModel

class AgentRequest(BaseModel):
    query: str
    llm_type: str = "openai"  # "openai" or "ollama"
    history: Optional[List[Tuple[str, str]]] = None  # [('role', 'content'), ...]

class AgentResponse(BaseModel):
    response: str
