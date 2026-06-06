from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.database.base import Base


class BusinessSettings(Base):
    __tablename__ = "business_settings"

    id = Column(Integer, primary_key=True, index=True)

    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False,
        unique=True
    )

    timezone = Column(
        String(100),
        nullable=False,
        default="Asia/Kolkata"
    )

    booking_rules = Column(
        String(500)
    )

    cancellation_policy = Column(
        String(500)
    )