from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.customer import Customer


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

def get_customer_by_phone(
    db: Session,
    business_id: int,
    phone: str
):
    validate_business(db, business_id)

    customer = (
        db.query(Customer)
        .filter(
            Customer.business_id == business_id,
            Customer.phone == phone
        )
        .first()
    )

    return customer

def create_customer_if_not_exists(
    db: Session,
    business_id: int,
    name: str,
    phone: str,
    email: str | None = None
):
    validate_business(db, business_id)

    customer = get_customer_by_phone(
        db,
        business_id,
        phone
    )

    if customer:
        return customer

    customer = Customer(
        business_id=business_id,
        name=name,
        phone=phone,
        email=email
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer

def get_customer(
    db: Session,
    business_id: int,
    customer_id: int
):
    validate_business(db, business_id)

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.business_id == business_id
        )
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer