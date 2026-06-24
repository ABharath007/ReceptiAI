from datetime import datetime
from pydantic import BaseModel


class ConversationSummaryCreate(BaseModel):
    session_id: int
    summary: str


class ConversationSummaryUpdate(BaseModel):
    session_id: int
    summary: str


class ConversationSummaryResponse(BaseModel):
    id: int
    session_id: int
    summary: str
    created_at: datetime

    class Config:
        from_attributes = True