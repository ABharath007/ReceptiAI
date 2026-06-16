from datetime import datetime, timedelta
from app.models.resource_availability import ResourceAvailability
from app.models.appointment import Appointment
from app.models.resource_leave import ResourceLeave

def get_available_slots(db, resource_id: int, appointment_date):
    """Returns all available slots for a resource on a specific date."""
    day_of_week = appointment_date.weekday() # Monday is 0 and Sunday is 6
    availability = (
        db.query(ResourceAvailability)
        .filter(
            ResourceAvailability.resource_id == resource_id,
            ResourceAvailability.day_of_week == day_of_week
        ).first()
    )
    if not availability:
        return []
    leave = (
        db.query(ResourceLeave)
        .filter(
            ResourceLeave.resource_id == resource_id,
            ResourceLeave.start_date <= appointment_date,
            ResourceLeave.end_date >= appointment_date
        ).first()
    )
    if leave:
        return []
    
    slots = []
    current_time = datetime.combine(appointment_date, availability.start_time)
    end_time = datetime.combine(appointment_date, availability.end_time)
    
    while current_time < end_time:
        slots.append(current_time.time())
        current_time += timedelta(minutes=availability.slot_duration)
    print(type(appointment_date))
    print(appointment_date)
    
    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.resource_id == resource_id,
            Appointment.appointment_date == appointment_date,
            Appointment.status == "BOOKED"
        ).all()
    )
    booked_slots = set()
    for appointment in appointments:
        current = datetime.combine(
        appointment_date,
        appointment.start_time
        )
        end = datetime.combine(
        appointment_date,
        appointment.end_time
        )
        while current < end:

            booked_slots.add(
            current.time())
            current += timedelta(
            minutes=availability.slot_duration)
    
    available_slots = [slot for slot in slots if slot not in booked_slots]
    return available_slots