from sqlalchemy.orm import Session

from app.models.appointment_status_history import AppointmentStatusHistory


def create_status_history(
    db: Session,
    appointment_id: int,
    old_status: str | None,
    new_status: str
):
    history = AppointmentStatusHistory(
        appointment_id=appointment_id,
        old_status=old_status,
        new_status=new_status
    )

    db.add(history)

    return history