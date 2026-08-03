from typing import Literal, Optional
from pydantic import BaseModel

class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str  

class ClearSessionRequest(BaseModel):
    session_id: str