from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)
from sqlalchemy.sql import func

from app.database.base import Base


class Ticket(Base):
    __tablename__ = "tickets"

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

    appointment_id = Column(
        Integer,
        ForeignKey("appointments.id")
    )

    subject = Column(
        String(255),
        nullable=False
    )

    description = Column(
        String(1000),
        nullable=False
    )

    status = Column(
        String(50),
        nullable=False,
        default="OPEN"
    )

    priority = Column(
        String(50),
        default="MEDIUM"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )