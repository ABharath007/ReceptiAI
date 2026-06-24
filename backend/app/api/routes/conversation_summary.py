from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.conversation_summary import ConversationSummary
from app.models.conversation_session import ConversationSession

from app.schemas.conversation_summary import (
    ConversationSummaryCreate,
    ConversationSummaryUpdate,
    ConversationSummaryResponse
)

router = APIRouter(
    prefix="/conversation-summaries",
    tags=["Conversation Summaries"]
)

@router.post(
    "/",
    response_model=ConversationSummaryResponse
)
def create_summary(
    summary_data: ConversationSummaryCreate,
    db: Session = Depends(get_db)
):

    session = (
        db.query(ConversationSession)
        .filter(
            ConversationSession.id == summary_data.session_id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Conversation session not found"
        )

    summary = ConversationSummary(
        session_id=summary_data.session_id,
        summary=summary_data.summary
    )

    db.add(summary)
    db.commit()
    db.refresh(summary)

    return summary

@router.get(
    "/",
    response_model=list[ConversationSummaryResponse]
)
def get_summaries(
    db: Session = Depends(get_db)
):
    return db.query(
        ConversationSummary
    ).all()
    
@router.get(
    "/{summary_id}",
    response_model=ConversationSummaryResponse
)
def get_summary(
    summary_id: int,
    db: Session = Depends(get_db)
):

    summary = (
        db.query(ConversationSummary)
        .filter(
            ConversationSummary.id == summary_id
        )
        .first()
    )

    if not summary:
        raise HTTPException(
            status_code=404,
            detail="Summary not found"
        )

    return summary

@router.put(
    "/{summary_id}",
    response_model=ConversationSummaryResponse
)
def update_summary(
    summary_id: int,
    summary_data: ConversationSummaryUpdate,
    db: Session = Depends(get_db)
):

    summary = (
        db.query(ConversationSummary)
        .filter(
            ConversationSummary.id == summary_id
        )
        .first()
    )

    if not summary:
        raise HTTPException(
            status_code=404,
            detail="Summary not found"
        )

    summary.session_id = summary_data.session_id
    summary.summary = summary_data.summary

    db.commit()
    db.refresh(summary)

    return summary

@router.delete(
    "/{summary_id}"
)
def delete_summary(
    summary_id: int,
    db: Session = Depends(get_db)
):

    summary = (
        db.query(ConversationSummary)
        .filter(
            ConversationSummary.id == summary_id
        )
        .first()
    )

    if not summary:
        raise HTTPException(
            status_code=404,
            detail="Summary not found"
        )

    db.delete(summary)
    db.commit()

    return {
        "message": "Summary deleted successfully"
    }