from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)
from sqlalchemy.sql import func

from app.database.base import Base


class AppointmentStatusHistory(Base):
    __tablename__ = "appointment_status_history"

    id = Column(Integer, primary_key=True, index=True)

    appointment_id = Column(
        Integer,
        ForeignKey("appointments.id"),
        nullable=False
    )

    old_status = Column(String(50))

    new_status = Column(
        String(50),
        nullable=False
    )

    changed_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )