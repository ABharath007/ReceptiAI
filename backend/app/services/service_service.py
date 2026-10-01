from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.service import Service


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


def get_service_by_name(
    db: Session,
    business_id: int,
    service_name: str
):
    validate_business(db, business_id)

    service = (
        db.query(Service)
        .filter(
            Service.business_id == business_id,
            Service.name.ilike(f"%{service_name}%"),
            Service.is_active == True
        )
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    return service