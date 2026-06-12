from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.service import Service
from app.models.business import Business
from app.schemas.service import (
    ServiceCreate,
    ServiceUpdate,
    ServiceResponse
)

router = APIRouter(
    prefix="/services",
    tags=["Services"]
)
@router.post("/", response_model=ServiceResponse)
def create_service(
    service: ServiceCreate,
    db: Session = Depends(get_db)
):
    business = db.query(Business).filter(Business.id == service.business_id).first()
    if not business:
        raise HTTPException(status_code=404,detail="Business not found")
    new_service = Service(
        business_id=service.business_id,
        name=service.name,
        description=service.description,
        duration_minutes=service.duration_minutes,
        price=service.price
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service

@router.get("/", response_model=list[ServiceResponse])
def get_services(
    db: Session = Depends(get_db)
):
    return db.query(Service).all()

@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    service = (
        db.query(Service)
        .filter(Service.id == service_id)
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    return service

@router.put("/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: int,
    service_data: ServiceUpdate,
    db: Session = Depends(get_db)
):
    service = (
        db.query(Service)
        .filter(Service.id == service_id)
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    service.business_id = service_data.business_id
    service.name = service_data.name
    service.description = service_data.description
    service.duration_minutes = service_data.duration_minutes
    service.price = service_data.price
    service.is_active = service_data.is_active

    db.commit()
    db.refresh(service)

    return service

@router.delete("/{service_id}")
def delete_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    service = (
        db.query(Service)
        .filter(Service.id == service_id)
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    db.delete(service)
    db.commit()

    return {
        "message": "Service deleted successfully"
    }