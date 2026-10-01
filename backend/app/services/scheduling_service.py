from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.resource_availability import ResourceAvailability
from app.models.appointment import Appointment
from app.models.resource_leave import ResourceLeave
from app.models.service import Service


def get_available_slots(
    db: Session,
    resource_id: int,
    appointment_date,
    service_id: int,
):
    """Return available start times for a service on a specific date."""

    service = (
        db.query(Service)
        .filter(
            Service.id == service_id,
            Service.is_active == True,
        )
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    day_of_week = appointment_date.weekday()

    availability = (
        db.query(ResourceAvailability)
        .filter(
            ResourceAvailability.resource_id == resource_id,
            ResourceAvailability.day_of_week == day_of_week,
        )
        .first()
    )

    if not availability:
        return []

    leave = (
        db.query(ResourceLeave)
        .filter(
            ResourceLeave.resource_id == resource_id,
            ResourceLeave.start_date <= appointment_date,
            ResourceLeave.end_date >= appointment_date,
        )
        .first()
    )

    if leave:
        return []

    working_start = datetime.combine(
        appointment_date,
        availability.start_time,
    )

    working_end = datetime.combine(
        appointment_date,
        availability.end_time,
    )

    service_duration = timedelta(
        minutes=service.duration_minutes
    )

    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.resource_id == resource_id,
            Appointment.appointment_date == appointment_date,
            Appointment.status == "BOOKED",
        )
        .all()
    )

    available_slots = []

    current_time = working_start

    while current_time + service_duration <= working_end:

        candidate_start = current_time
        candidate_end = current_time + service_duration

        has_conflict = False

        for appointment in appointments:
            existing_start = datetime.combine(
                appointment_date,
                appointment.start_time,
            )

            existing_end = datetime.combine(
                appointment_date,
                appointment.end_time,
            )

            if (
                candidate_start < existing_end
                and candidate_end > existing_start
            ):
                has_conflict = True
                break

        if not has_conflict:
            available_slots.append(candidate_start.time())

        current_time += timedelta(
            minutes=availability.slot_duration
        )

    return available_slots