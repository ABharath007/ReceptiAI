from pydantic import BaseModel, EmailStr
from datetime import datetime


class CustomerCreate(BaseModel):
    business_id: int
    name: str
    phone: str
    email: EmailStr | None = None


class CustomerResponse(BaseModel):
    id: int
    business_id: int
    name: str
    phone: str
    email: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
        
class CustomerUpdate(BaseModel):
    business_id: int
    name: str
    phone: str
    email: EmailStr | None = None