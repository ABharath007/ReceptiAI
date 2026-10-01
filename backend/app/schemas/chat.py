from pydantic import BaseModel


class ChatRequest(BaseModel):
    business_id: int
    message: str
    session_id: int | None = None


class ChatResponse(BaseModel):
    response: str
    session_id: int | None = None