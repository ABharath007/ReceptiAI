from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    Time,
    DateTime
)
from sqlalchemy.sql import func

from app.database.base import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    resource_id = Column(
        Integer,
        ForeignKey("resources.id"),
        nullable=False
    )

    appointment_date = Column(
        Date,
        nullable=False
    )

    start_time = Column(
        Time,
        nullable=False
    )

    end_time = Column(
        Time,
        nullable=False
    )

    status = Column(
        String(50),
        nullable=False,
        default="BOOKED"
    )

    special_notes = Column(String(1000))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )