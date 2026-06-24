from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.conversation_session import ConversationSession
from app.models.business import Business
from app.models.customer import Customer

from app.schemas.conversation_session import (
    ConversationSessionCreate,
    ConversationSessionUpdate,
    ConversationSessionResponse
)

router = APIRouter(
    prefix="/conversation-sessions",
    tags=["Conversation Sessions"]
)

@router.post(
    "/",
    response_model=ConversationSessionResponse
)
def create_conversation_session(
    session_data: ConversationSessionCreate,
    db: Session = Depends(get_db)
):

    business = (
        db.query(Business)
        .filter(Business.id == session_data.business_id)
        .first()
    )

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == session_data.customer_id,
            Customer.business_id == session_data.business_id
        )
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    conversation = ConversationSession(
        business_id=session_data.business_id,
        customer_id=session_data.customer_id
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation

@router.get(
    "/",
    response_model=list[ConversationSessionResponse]
)
def get_conversation_sessions(
    db: Session = Depends(get_db)
):
    return db.query(
        ConversationSession
    ).all()
    
@router.get(
    "/{session_id}",
    response_model=ConversationSessionResponse
)
def get_conversation_session(
    session_id: int,
    db: Session = Depends(get_db)
):

    conversation = (
        db.query(ConversationSession)
        .filter(
            ConversationSession.id == session_id
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation session not found"
        )

    return conversation

@router.put(
    "/{session_id}",
    response_model=ConversationSessionResponse
)
def update_conversation_session(
    session_id: int,
    session_data: ConversationSessionUpdate,
    db: Session = Depends(get_db)
):

    conversation = (
        db.query(ConversationSession)
        .filter(
            ConversationSession.id == session_id
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation session not found"
        )

    conversation.business_id = session_data.business_id
    conversation.customer_id = session_data.customer_id
    conversation.ended_at = session_data.ended_at

    db.commit()
    db.refresh(conversation)

    return conversation

@router.delete(
    "/{session_id}"
)
def delete_conversation_session(
    session_id: int,
    db: Session = Depends(get_db)
):

    conversation = (
        db.query(ConversationSession)
        .filter(
            ConversationSession.id == session_id
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation session not found"
        )

    db.delete(conversation)
    db.commit()

    return {
        "message": "Conversation session deleted successfully"
    }