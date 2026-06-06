from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Text
)
from sqlalchemy.sql import func

from app.database.base import Base


class ConversationSummary(Base):
    __tablename__ = "conversation_summaries"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(
        Integer,
        ForeignKey("conversation_sessions.id"),
        nullable=False
    )

    summary = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )