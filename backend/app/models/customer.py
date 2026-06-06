from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)
from sqlalchemy.sql import func

from app.database.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False
    )

    name = Column(String(255), nullable=False)

    phone = Column(
        String(20),
        nullable=False
    )

    email = Column(String(255))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )