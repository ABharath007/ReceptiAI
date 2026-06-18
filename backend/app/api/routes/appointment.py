from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.appointment import Appointment
from app.models.business import Business
from app.models.customer import Customer
from app.models.resource import Resource

from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse
)
from app.services.booking_service import create_booking

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)

@router.post(
    "/",
    response_model=AppointmentResponse
)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)):

    return create_booking(
    db=db,
    business_id=appointment.business_id,
    customer_id=appointment.customer_id,
    resource_id=appointment.resource_id,
    appointment_date=appointment.appointment_date,
    start_time=appointment.start_time,
    end_time=appointment.end_time,
    special_notes=appointment.special_notes
)

@router.get(
    "/",
    response_model=list[AppointmentResponse]
)
def get_appointments(
    db: Session = Depends(get_db)
):
    return db.query(
        Appointment
    ).all()
    
@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse
)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id
        )
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return appointment

@router.put(
    "/{appointment_id}",
    response_model=AppointmentResponse
)
def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id
        )
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    appointment.business_id = appointment_data.business_id
    appointment.customer_id = appointment_data.customer_id
    appointment.resource_id = appointment_data.resource_id
    appointment.appointment_date = appointment_data.appointment_date
    appointment.start_time = appointment_data.start_time
    appointment.end_time = appointment_data.end_time
    appointment.status = appointment_data.status
    appointment.special_notes = appointment_data.special_notes

    db.commit()
    db.refresh(appointment)

    return appointment

@router.delete(
    "/{appointment_id}"
)
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id
        )
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    db.delete(appointment)
    db.commit()

    return {
        "message": "Appointment deleted successfully"
    }