from datetime import datetime
from pydantic import BaseModel


class ConversationSessionCreate(BaseModel):
    business_id: int
    customer_id: int


class ConversationSessionUpdate(BaseModel):
    business_id: int
    customer_id: int
    ended_at: datetime | None = None


class ConversationSessionResponse(BaseModel):
    id: int
    business_id: int
    customer_id: int
    started_at: datetime
    ended_at: datetime | None = None

    class Config:
        from_attributes = True