from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.business import Business
from app.schemas.business import BusinessCreate, BusinessResponse, BusinessUpdate

router = APIRouter(
    prefix="/businesses",
    tags=["businesses"]
)

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

@router.get("/", response_model=list[BusinessResponse])
def get_businesses(db: Session = Depends(get_db)):
    return db.query(Business).all()

@router.get("/{business_id}", response_model=BusinessResponse)
def get_business(business_id: int, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business
@router.put("/{business_id}", response_model=BusinessResponse)
def update_business(business_id: int, business_data: BusinessUpdate, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    business.name = business_data.name
    business.industry = business_data.industry
    business.phone = business_data.phone
    business.email = business_data.email
    business.address = business_data.address
    
    db.commit()
    db.refresh(business)
    return business

@router.delete("/{business_id}")
def delete_business(business_id: int, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    db.delete(business)
    db.commit()
    return {"detail": "Business deleted successfully"}