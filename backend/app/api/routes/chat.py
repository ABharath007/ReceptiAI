from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ai.agent import invoke_agent
from app.schemas.chat import ChatRequest, ChatResponse
from app.database.database import get_db


router = APIRouter(prefix="/chat", tags=["AI Chat"])


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    result = invoke_agent(
        message=request.message,
        business_id=request.business_id,
        db=db,
        session_id=request.session_id
    )

    return ChatResponse(
        response=result["response"],
        session_id=result["session_id"])