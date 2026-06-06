from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text
)

from app.database.base import Base


class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    id = Column(Integer, primary_key=True, index=True)

    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False
    )

    category = Column(
        String(100),
        nullable=False
    )

    title = Column(
        String(255),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )