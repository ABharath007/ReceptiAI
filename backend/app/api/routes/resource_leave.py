from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.resource_leave import ResourceLeave
from app.models.resource import Resource

from app.schemas.resource_leave import (
    ResourceLeaveCreate,
    ResourceLeaveUpdate,
    ResourceLeaveResponse
)

router = APIRouter(
    prefix="/resource-leaves",
    tags=["Resource Leaves"]
)

@router.post(
    "/",
    response_model=ResourceLeaveResponse
)
def create_resource_leave(
    leave: ResourceLeaveCreate,
    db: Session = Depends(get_db)
):
    resource = (
        db.query(Resource)
        .filter(Resource.id == leave.resource_id)
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    new_leave = ResourceLeave(
        resource_id=leave.resource_id,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason
    )

    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)

    return new_leave

@router.get(
    "/",
    response_model=list[ResourceLeaveResponse]
)
def get_resource_leaves(
    db: Session = Depends(get_db)
):
    return db.query(
        ResourceLeave
    ).all()
    
@router.get(
    "/{leave_id}",
    response_model=ResourceLeaveResponse
)
def get_resource_leave(
    leave_id: int,
    db: Session = Depends(get_db)
):
    leave = (
        db.query(ResourceLeave)
        .filter(ResourceLeave.id == leave_id)
        .first()
    )

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave not found"
        )

    return leave

@router.put(
    "/{leave_id}",
    response_model=ResourceLeaveResponse
)
def update_resource_leave(
    leave_id: int,
    leave_data: ResourceLeaveUpdate,
    db: Session = Depends(get_db)
):
    leave = (
        db.query(ResourceLeave)
        .filter(ResourceLeave.id == leave_id)
        .first()
    )

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave not found"
        )

    leave.resource_id = leave_data.resource_id
    leave.start_date = leave_data.start_date
    leave.end_date = leave_data.end_date
    leave.reason = leave_data.reason

    db.commit()
    db.refresh(leave)

    return leave

@router.delete(
    "/{leave_id}"
)
def delete_resource_leave(
    leave_id: int,
    db: Session = Depends(get_db)
):
    leave = (
        db.query(ResourceLeave)
        .filter(ResourceLeave.id == leave_id)
        .first()
    )

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave not found"
        )

    db.delete(leave)
    db.commit()

    return {
        "message": "Leave deleted successfully"
    }