from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)

from app.database.base import Base


class ResourceService(Base):
    __tablename__ = "resource_services"

    id = Column(Integer, primary_key=True, index=True)

    resource_id = Column(
        Integer,
        ForeignKey("resources.id"),
        nullable=False
    )

    service_id = Column(
        Integer,
        ForeignKey("services.id"),
        nullable=False
    )