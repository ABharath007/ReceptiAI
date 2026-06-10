from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.business import Business
from app.schemas.business import BusinessCreate, BusinessResponse

router = APIRouter(
    prefix="/businesses",
    tags=["businesses"]
)

@router.get("/")
def get_businesses():
    return {"message": "List of businesses"}

@router.post("/", response_model=BusinessResponse)
def create_business(business: BusinessCreate, db: Session = Depends(get_db)):
    new_business = Business(
        name=business.name,
        industry=business.industry,
        phone = business.phone,
        email = business.email,
        address = business.address
    )
    db.add(new_business)
    db.commit()
    db.refresh(new_business)
    return new_business