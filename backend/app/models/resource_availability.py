from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Time
)

from app.database.base import Base


class ResourceAvailability(Base):
    __tablename__ = "resource_availability"

    id = Column(Integer, primary_key=True, index=True)

    resource_id = Column(
        Integer,
        ForeignKey("resources.id"),
        nullable=False
    )

    day_of_week = Column(
        String(20),
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

    slot_duration = Column(
        Integer,
        nullable=False
    )