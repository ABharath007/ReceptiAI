from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.resource_availability import ResourceAvailability
from app.schemas.resource_availability import (
    ResourceAvailabilityCreate,
    ResourceAvailabilityResponse,
    ResourceAvailabilityUpdate
)
from app.models.resource import Resource

router = APIRouter(
    prefix="/resource-availability",
    tags = ["Resource Availability"])

@router.post("/", response_model=ResourceAvailabilityResponse)
def create_resource_availability(
    availability: ResourceAvailabilityCreate,
    db: Session = Depends(get_db)
):
    resource = db.query(Resource).filter(Resource.id == availability.resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    new_availability = ResourceAvailability(
        resource_id=availability.resource_id,
        day_of_week=availability.day_of_week,
        start_time=availability.start_time,
        end_time=availability.end_time,
        slot_duration = availability.slot_duration
    )

    db.add(new_availability)
    db.commit()
    db.refresh(new_availability)

    return new_availability

@router.get("/", response_model = list[ResourceAvailabilityResponse])
def get_resource_availability( db: Session = Depends(get_db)):
    return db.query(ResourceAvailability).all()

@router.get("/{availability_id}",response_model = ResourceAvailabilityResponse)
def get_resource_availability_by_id(availability_id: int, db: Session=Depends(get_db)):
    availability = (db.query(ResourceAvailability).filter(ResourceAvailability.id == availability_id).first())
    if not availability:
        raise HTTPException(status_code = 404,detail = "Availability not found")
    return availability

@router.put("/{availability_id}", response_model = ResourceAvailabilityResponse)
def update_resource_availability(availability_id : int, availability_data: ResourceAvailabilityUpdate, db:Session = Depends(get_db)):
    availability = (db.query(ResourceAvailability).filter(ResourceAvailability.id == availability_id).first())
    if not availability:
        raise HTTPException(status_code = 404, detail = "Availability not found")
    availability.resource_id = availability_data.resource_id
    availability.day_of_week = availability_data.day_of_week
    availability.start_time = availability_data.start_time
    availability.end_time = availability_data.end_time
    availability.slot_duration = availability_data.slot_duration
    db.commit()
    db.refresh(availability)
    return availability

@router.delete("/{availability_id}")
def delete_resource_availability(availability_id :int, db: Session = Depends(get_db)):
    availability = (db.query(ResourceAvailability).filter(ResourceAvailability.id == availability_id).first())
    if not availability:
        raise HTTPException(status_code = 404, detail = "Availability not found")
    db.delete(availability)
    db.commit()
    return {"message": "Availability deleted Successfully"}