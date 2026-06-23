from pydantic import BaseModel


class ResourceServiceCreate(BaseModel):
    resource_id: int
    service_id: int


class ResourceServiceUpdate(BaseModel):
    resource_id: int
    service_id: int


class ResourceServiceResponse(BaseModel):
    id: int
    resource_id: int
    service_id: int

    class Config:
        from_attributes = True