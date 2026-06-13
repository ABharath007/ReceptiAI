from pydantic import BaseModel
from datetime import date, time, datetime


class AppointmentCreate(BaseModel):
    business_id: int
    customer_id: int
    resource_id: int
    appointment_date: date
    start_time: time
    end_time: time
    special_notes: str | None = None


class AppointmentUpdate(BaseModel):
    business_id: int
    customer_id: int
    resource_id: int
    appointment_date: date
    start_time: time
    end_time: time
    status: str
    special_notes: str | None = None


class AppointmentResponse(BaseModel):
    id: int
    business_id: int
    customer_id: int
    resource_id: int
    appointment_date: date
    start_time: time
    end_time: time
    status: str
    special_notes: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True