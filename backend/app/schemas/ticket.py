from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TicketCreate(BaseModel):
    business_id: int
    customer_id: int
    appointment_id: Optional[int] = None
    subject: str
    description: str
    priority: str = "MEDIUM"


class TicketUpdate(BaseModel):
    business_id: int
    customer_id: int
    appointment_id: Optional[int] = None
    subject: str
    description: str
    status: str
    priority: str


class TicketResponse(BaseModel):
    id: int
    business_id: int
    customer_id: int
    appointment_id: Optional[int]
    subject: str
    description: str
    status: str
    priority: str
    created_at: datetime

    class Config:
        from_attributes = True