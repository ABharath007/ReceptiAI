from pydantic import BaseModel
from datetime import time

class ResourceAvailabilityCreate(BaseModel):
    resource_id: int
    day_of_week: int
    start_time: time
    end_time: time
    slot_duration: int
    
class ResourceAvailabilityUpdate(BaseModel):
    resource_id: int
    day_of_week: int
    start_time: time
    end_time: time
    slot_duration: int
    
class ResourceAvailabilityResponse(BaseModel):
    id: int
    resource_id: int
    day_of_week: int
    start_time: time
    end_time: time
    slot_duration: int

    class Config:
        from_attributes = True