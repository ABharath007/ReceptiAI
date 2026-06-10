from pydantic import BaseModel
from datetime import datetime


class ResourceCreate(BaseModel):
    business_id: int
    name: str
    resource_type: str
    bio: str | None = None
    experience_years: int | None = None


class ResourceResponse(BaseModel):
    id: int
    business_id: int
    name: str
    resource_type: str
    bio: str | None = None
    experience_years: int | None = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True