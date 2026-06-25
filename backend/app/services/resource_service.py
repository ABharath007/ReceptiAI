from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.resource import Resource
from app.models.service import Service
from app.models.resource_service import ResourceService


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


def get_resources_by_service(
    db: Session,
    business_id: int,
    service_id: int
):
    validate_business(db, business_id)

    service = (
        db.query(Service)
        .filter(
            Service.id == service_id,
            Service.business_id == business_id
        )
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    resources = (
        db.query(Resource)
        .join(
            ResourceService,
            Resource.id == ResourceService.resource_id
        )
        .filter(
            Resource.business_id == business_id,
            ResourceService.service_id == service_id
        )
        .all()
    )

    return resources


def get_services_by_resource(
    db: Session,
    business_id: int,
    resource_id: int
):
    validate_business(db, business_id)

    resource = (
        db.query(Resource)
        .filter(
            Resource.id == resource_id,
            Resource.business_id == business_id
        )
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    services = (
        db.query(Service)
        .join(
            ResourceService,
            Service.id == ResourceService.service_id
        )
        .filter(
            ResourceService.resource_id == resource_id,
            Service.business_id == business_id
        )
        .all()
    )

    return services


def get_resource_by_name(
    db: Session,
    business_id: int,
    resource_name: str
):
    validate_business(db, business_id)

    resource = (
        db.query(Resource)
        .filter(
            Resource.business_id == business_id,
            Resource.name.ilike(f"%{resource_name}%")
        )
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    return resource