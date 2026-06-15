from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.scheduling_service import get_available_slots

router = APIRouter(
    prefix="/scheduling",
    tags=["Scheduling"]
)

@router.get("/available-slots/{resource_id}")
def available_slots(
    resource_id: int,
    appointment_date: date,
    db: Session = Depends(get_db)
):
    slots = get_available_slots(db=db, resource_id=resource_id, appointment_date=appointment_date)
    if not slots:
        raise HTTPException(
            status_code=404,
            detail="No available slots found for the given resource and date"
        )
    return {
        "resource_id": resource_id,
        "appointment_date": appointment_date,
        "available_slots": slots
    }