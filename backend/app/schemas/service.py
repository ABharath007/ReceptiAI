from pydantic import BaseModel
from datetime import datetime


class ServiceCreate(BaseModel):
    business_id: int
    name: str
    description: str | None = None
    duration_minutes: int
    price: int


class ServiceResponse(BaseModel):
    id: int
    business_id: int
    name: str
    description: str | None = None
    duration_minutes: int
    price: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True