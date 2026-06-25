from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.business import Business
from app.models.knowledge_base import KnowledgeBase


def get_all_knowledge(
    db: Session,
    business_id: int
):
    validate_business(db, business_id)

    return (
        db.query(KnowledgeBase)
        .filter(
            KnowledgeBase.business_id == business_id
        )
        .all()
    )
    
def get_knowledge_by_category(
    db: Session,
    business_id: int,
    category: str
):

    validate_business(db, business_id)

    return (
        db.query(KnowledgeBase)
        .filter(
            KnowledgeBase.business_id == business_id,
            KnowledgeBase.category.ilike(f"%{category}%")
        )
        .all()
    )
    
def search_knowledge(
    db: Session,
    business_id: int,
    query: str
):

    validate_business(db, business_id)

    results = (
        db.query(KnowledgeBase)
        .filter(
            KnowledgeBase.business_id == business_id,
            or_(
                KnowledgeBase.category.ilike(f"%{query}%"),
                KnowledgeBase.title.ilike(f"%{query}%"),
                KnowledgeBase.content.ilike(f"%{query}%")
            )
        )
        .all()
    )

    return results

def validate_business(db: Session, business_id: int):
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