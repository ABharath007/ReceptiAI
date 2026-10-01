from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date, time, datetime, timedelta

from app.models.business import Business
from app.models.customer import Customer
from app.models.resource import Resource
from app.models.service import Service
from app.models.resource_service import ResourceService
from app.models.appointment import Appointment

from app.services.scheduling_service import get_available_slots
from app.services.status_history_service import create_status_history


def create_booking(
    db: Session,
    business_id: int,
    customer_id: int,
    resource_id: int,
    service_id: int,
    appointment_date: date,
    start_time: time,
    special_notes: str | None = None,
):
    business = (
        db.query(Business)
        .filter(Business.id == business_id)
        .first()
    )

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.business_id == business_id,
        )
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    resource = (
        db.query(Resource)
        .filter(
            Resource.id == resource_id,
            Resource.business_id == business_id,
        )
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    service = (
        db.query(Service)
        .filter(
            Service.id == service_id,
            Service.business_id == business_id,
            Service.is_active == True,
        )
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    resource_service = (
        db.query(ResourceService)
        .filter(
            ResourceService.resource_id == resource_id,
            ResourceService.service_id == service_id,
        )
        .first()
    )

    if not resource_service:
        raise HTTPException(
            status_code=409,
            detail="This resource does not provide the selected service"
        )

    end_datetime = (
        datetime.combine(appointment_date, start_time)
        + timedelta(minutes=service.duration_minutes)
    )

    end_time = end_datetime.time()

    available_slots = get_available_slots(
        db=db,
        resource_id=resource_id,
        service_id=service_id,
        appointment_date=appointment_date,
    )

    if start_time not in available_slots:
        raise HTTPException(
            status_code=409,
            detail="Selected slot is no longer available"
        )

    appointment = Appointment(
        business_id=business_id,
        customer_id=customer_id,
        resource_id=resource_id,
        appointment_date=appointment_date,
        start_time=start_time,
        end_time=end_time,
        special_notes=special_notes,
        status="BOOKED",
    )

    db.add(appointment)
    db.flush()

    create_status_history(
        db=db,
        appointment_id=appointment.id,
        old_status=None,
        new_status="BOOKED",
    )

    db.commit()
    db.refresh(appointment)

    return appointment