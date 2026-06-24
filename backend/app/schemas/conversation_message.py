from datetime import datetime
from pydantic import BaseModel


class ConversationMessageCreate(BaseModel):
    session_id: int
    sender: str
    message: str


class ConversationMessageUpdate(BaseModel):
    session_id: int
    sender: str
    message: str


class ConversationMessageResponse(BaseModel):
    id: int
    session_id: int
    sender: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True