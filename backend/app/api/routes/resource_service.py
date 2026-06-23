from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.resource_service import ResourceService
from app.models.resource import Resource
from app.models.service import Service

from app.schemas.resource_service import (
    ResourceServiceCreate,
    ResourceServiceUpdate,
    ResourceServiceResponse
)

router = APIRouter(
    prefix="/resource-services",
    tags=["Resource Services"]
)


@router.post(
    "/",
    response_model=ResourceServiceResponse
)
def create_resource_service(
    resource_service: ResourceServiceCreate,
    db: Session = Depends(get_db)
):

    resource = db.query(Resource).filter(
        Resource.id == resource_service.resource_id
    ).first()

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    service = db.query(Service).filter(
        Service.id == resource_service.service_id
    ).first()

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    existing = db.query(ResourceService).filter(
        ResourceService.resource_id == resource_service.resource_id,
        ResourceService.service_id == resource_service.service_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Resource is already mapped to this service"
        )

    new_mapping = ResourceService(
        resource_id=resource_service.resource_id,
        service_id=resource_service.service_id
    )

    db.add(new_mapping)
    db.commit()
    db.refresh(new_mapping)

    return new_mapping


@router.get(
    "/",
    response_model=list[ResourceServiceResponse]
)
def get_resource_services(
    db: Session = Depends(get_db)
):
    return db.query(ResourceService).all()


@router.get(
    "/{mapping_id}",
    response_model=ResourceServiceResponse
)
def get_resource_service(
    mapping_id: int,
    db: Session = Depends(get_db)
):

    mapping = db.query(ResourceService).filter(
        ResourceService.id == mapping_id
    ).first()

    if not mapping:
        raise HTTPException(
            status_code=404,
            detail="Mapping not found"
        )

    return mapping


@router.put(
    "/{mapping_id}",
    response_model=ResourceServiceResponse
)
def update_resource_service(
    mapping_id: int,
    mapping_data: ResourceServiceUpdate,
    db: Session = Depends(get_db)
):

    mapping = db.query(ResourceService).filter(
        ResourceService.id == mapping_id
    ).first()

    if not mapping:
        raise HTTPException(
            status_code=404,
            detail="Mapping not found"
        )

    mapping.resource_id = mapping_data.resource_id
    mapping.service_id = mapping_data.service_id

    db.commit()
    db.refresh(mapping)

    return mapping


@router.delete(
    "/{mapping_id}"
)
def delete_resource_service(
    mapping_id: int,
    db: Session = Depends(get_db)
):

    mapping = db.query(ResourceService).filter(
        ResourceService.id == mapping_id
    ).first()

    if not mapping:
        raise HTTPException(
            status_code=404,
            detail="Mapping not found"
        )

    db.delete(mapping)
    db.commit()

    return {
        "message": "Mapping deleted successfully"
    }