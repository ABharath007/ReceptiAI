from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.resource import Resource
from app.schemas.resource import (
    ResourceCreate,
    ResourceUpdate,
    ResourceResponse
)

router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)

@router.post("/", response_model=ResourceResponse)
def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db)
):
    new_resource = Resource(
        business_id=resource.business_id,
        name=resource.name,
        resource_type=resource.resource_type,
        bio=resource.bio,
        experience_years=resource.experience_years
    )

    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)

    return new_resource

@router.get("/", response_model=list[ResourceResponse])
def get_resources(
    db: Session = Depends(get_db)
):
    return db.query(Resource).all()

@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(
    resource_id: int,
    db: Session = Depends(get_db)
):
    resource = (
        db.query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    return resource

@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    db: Session = Depends(get_db)
):
    resource = (
        db.query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )
    resource.business_id = resource_data.business_id
    resource.name = resource_data.name
    resource.resource_type = resource_data.resource_type
    resource.bio = resource_data.bio
    resource.experience_years = resource_data.experience_years
    resource.is_active = resource_data.is_active

    db.commit()
    db.refresh(resource)

    return resource

@router.delete("/{resource_id}")
def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db)
):
    resource = (
        db.query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    db.delete(resource)
    db.commit()

    return {
        "message": "Resource deleted successfully"
    }