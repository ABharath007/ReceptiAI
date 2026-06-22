from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.services.status_history_service import create_status_history


def update_appointment_status( db: Session, appointment_id: int, new_status:str):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code = 404, detail = "Appointment not found")
    old_status = appointment.status
    if old_status == new_status:
        raise HTTPException(status_code = 400, detail = "Appointment is already in the desired status")
    appointment.status = new_status
    create_status_history(db=db, appointment_id=appointment.id, old_status=old_status, new_status=new_status)
    return appointment