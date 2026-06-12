from pydantic import BaseModel
from datetime import date


class ResourceLeaveCreate(BaseModel):
    resource_id: int
    start_date: date
    end_date: date
    reason: str | None = None


class ResourceLeaveUpdate(BaseModel):
    resource_id: int
    start_date: date
    end_date: date
    reason: str | None = None


class ResourceLeaveResponse(BaseModel):
    id: int
    resource_id: int
    start_date: date
    end_date: date
    reason: str | None = None

    class Config:
        from_attributes = True