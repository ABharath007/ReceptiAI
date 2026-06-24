from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.conversation_message import ConversationMessage
from app.models.conversation_session import ConversationSession

from app.schemas.conversation_message import (
    ConversationMessageCreate,
    ConversationMessageUpdate,
    ConversationMessageResponse
)

router = APIRouter(
    prefix="/conversation-messages",
    tags=["Conversation Messages"]
)

@router.post(
    "/",
    response_model=ConversationMessageResponse
)
def create_message(
    message_data: ConversationMessageCreate,
    db: Session = Depends(get_db)
):

    session = (
        db.query(ConversationSession)
        .filter(
            ConversationSession.id == message_data.session_id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Conversation session not found"
        )

    message = ConversationMessage(
        session_id=message_data.session_id,
        sender=message_data.sender,
        message=message_data.message
    )

    db.add(message)
    db.commit()
    db.refresh(message)
    
    return message

@router.get(
    "/",
    response_model=list[ConversationMessageResponse]
)
def get_messages(
    db: Session = Depends(get_db)
):
    return db.query(
        ConversationMessage
    ).all()
    
@router.get(
    "/{message_id}",
    response_model=ConversationMessageResponse
)
def get_message(
    message_id: int,
    db: Session = Depends(get_db)
):

    message = (
        db.query(ConversationMessage)
        .filter(
            ConversationMessage.id == message_id
        )
        .first()
    )

    if not message:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )

    return message

@router.put(
    "/{message_id}",
    response_model=ConversationMessageResponse
)
def update_message(
    message_id: int,
    message_data: ConversationMessageUpdate,
    db: Session = Depends(get_db)
):

    message = (
        db.query(ConversationMessage)
        .filter(
            ConversationMessage.id == message_id
        )
        .first()
    )

    if not message:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )

    message.session_id = message_data.session_id
    message.sender = message_data.sender
    message.message = message_data.message

    db.commit()
    db.refresh(message)

    return message

@router.delete(
    "/{message_id}"
)
def delete_message(
    message_id: int,
    db: Session = Depends(get_db)
):

    message = (
        db.query(ConversationMessage)
        .filter(
            ConversationMessage.id == message_id
        )
        .first()
    )

    if not message:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )

    db.delete(message)
    db.commit()

    return {
        "message": "Message deleted successfully"
    }