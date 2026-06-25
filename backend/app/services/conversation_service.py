from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.business import Business
from app.models.customer import Customer

from app.models.conversation_session import ConversationSession
from app.models.conversation_message import ConversationMessage
from app.models.conversation_summary import ConversationSummary


def validate_business(
    db: Session,
    business_id: int
):
    business = (
        db.query(Business)
        .filter(Business.id == business_id)
        .first()
    )

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    return business


def create_session(
    db: Session,
    business_id: int,
    customer_id: int
):
    validate_business(db, business_id)

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.business_id == business_id
        )
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    session = ConversationSession(
        business_id=business_id,
        customer_id=customer_id
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def add_message(
    db: Session,
    session_id: int,
    sender: str,
    message: str
):
    session = (
        db.query(ConversationSession)
        .filter(
            ConversationSession.id == session_id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Conversation session not found"
        )

    conversation_message = ConversationMessage(
        session_id=session_id,
        sender=sender,
        message=message
    )

    db.add(conversation_message)
    db.commit()
    db.refresh(conversation_message)

    return conversation_message


def create_summary(
    db: Session,
    session_id: int,
    summary: str
):
    session = (
        db.query(ConversationSession)
        .filter(
            ConversationSession.id == session_id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Conversation session not found"
        )

    conversation_summary = ConversationSummary(
        session_id=session_id,
        summary=summary
    )

    db.add(conversation_summary)
    db.commit()
    db.refresh(conversation_summary)

    return conversation_summary


def end_session(
    db: Session,
    session_id: int,
    ended_at: datetime
):
    session = (
        db.query(ConversationSession)
        .filter(
            ConversationSession.id == session_id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Conversation session not found"
        )

    session.ended_at = ended_at

    db.commit()
    db.refresh(session)

    return session