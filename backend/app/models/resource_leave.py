from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date
)

from app.database.base import Base


class ResourceLeave(Base):
    __tablename__ = "resource_leaves"

    id = Column(Integer, primary_key=True, index=True)

    resource_id = Column(
        Integer,
        ForeignKey("resources.id"),
        nullable=False
    )

    start_date = Column(
        Date,
        nullable=False
    )

    end_date = Column(
        Date,
        nullable=False
    )

    reason = Column(String(255))