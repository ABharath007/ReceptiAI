from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.business import Business
from app.models.knowledge_base import KnowledgeBase

from app.schemas.knowledge_base import (
    KnowledgeBaseCreate,
    KnowledgeBaseUpdate,
    KnowledgeBaseResponse
)

router = APIRouter(
    prefix="/knowledge-base",
    tags=["Knowledge Base"]
)


@router.post(
    "/",
    response_model=KnowledgeBaseResponse
)
def create_knowledge(
    knowledge: KnowledgeBaseCreate,
    db: Session = Depends(get_db)
):

    business = (
        db.query(Business)
        .filter(Business.id == knowledge.business_id)
        .first()
    )

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    new_knowledge = KnowledgeBase(
        business_id=knowledge.business_id,
        category=knowledge.category,
        title=knowledge.title,
        content=knowledge.content
    )

    db.add(new_knowledge)
    db.commit()
    db.refresh(new_knowledge)

    return new_knowledge


@router.get(
    "/",
    response_model=list[KnowledgeBaseResponse]
)
def get_knowledge(
    db: Session = Depends(get_db)
):
    return db.query(KnowledgeBase).all()


@router.get(
    "/{knowledge_id}",
    response_model=KnowledgeBaseResponse
)
def get_knowledge_by_id(
    knowledge_id: int,
    db: Session = Depends(get_db)
):

    knowledge = (
        db.query(KnowledgeBase)
        .filter(KnowledgeBase.id == knowledge_id)
        .first()
    )

    if not knowledge:
        raise HTTPException(
            status_code=404,
            detail="Knowledge not found"
        )

    return knowledge


@router.put(
    "/{knowledge_id}",
    response_model=KnowledgeBaseResponse
)
def update_knowledge(
    knowledge_id: int,
    knowledge_data: KnowledgeBaseUpdate,
    db: Session = Depends(get_db)
):

    knowledge = (
        db.query(KnowledgeBase)
        .filter(KnowledgeBase.id == knowledge_id)
        .first()
    )

    if not knowledge:
        raise HTTPException(
            status_code=404,
            detail="Knowledge not found"
        )

    knowledge.business_id = knowledge_data.business_id
    knowledge.category = knowledge_data.category
    knowledge.title = knowledge_data.title
    knowledge.content = knowledge_data.content

    db.commit()
    db.refresh(knowledge)

    return knowledge


@router.delete(
    "/{knowledge_id}"
)
def delete_knowledge(
    knowledge_id: int,
    db: Session = Depends(get_db)
):

    knowledge = (
        db.query(KnowledgeBase)
        .filter(KnowledgeBase.id == knowledge_id)
        .first()
    )

    if not knowledge:
        raise HTTPException(
            status_code=404,
            detail="Knowledge not found"
        )

    db.delete(knowledge)
    db.commit()

    return {
        "message": "Knowledge deleted successfully"
    }