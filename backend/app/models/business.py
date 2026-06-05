from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.base import Base

class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    industry = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    address = Column(String(500))
    verification_status = Column(
    String(50),
    nullable=False,
    default="PENDING"
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )