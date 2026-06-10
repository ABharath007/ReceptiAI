from pydantic import BaseModel, EmailStr
from datetime import datetime

class BusinessCreate(BaseModel):
    name: str
    industry: str
    phone : str
    email: EmailStr
    address: str | None = None
    
class BusinessResponse(BaseModel):
    id : int
    name: str
    industry: str
    phone : str
    email: EmailStr
    address: str | None = None
    verification_status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class BusinessUpdate(BaseModel):
    name:str
    industry:str
    phone : str
    email: EmailStr
    address: str | None = None