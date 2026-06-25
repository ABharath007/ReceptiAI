from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.customer import Customer
from app.models.appointment import Appointment
from app.models.ticket import Ticket


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


def create_ticket(
    db: Session,
    business_id: int,
    customer_id: int,
    subject: str,
    description: str,
    appointment_id: int | None = None,
    priority: str = "MEDIUM"
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

    if appointment_id is not None:

        appointment = (
            db.query(Appointment)
            .filter(
                Appointment.id == appointment_id,
                Appointment.business_id == business_id
            )
            .first()
        )

        if not appointment:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found"
            )

    ticket = Ticket(
        business_id=business_id,
        customer_id=customer_id,
        appointment_id=appointment_id,
        subject=subject,
        description=description,
        priority=priority,
        status="OPEN"
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


def close_ticket(
    db: Session,
    business_id: int,
    ticket_id: int
):
    validate_business(db, business_id)

    ticket = (
        db.query(Ticket)
        .filter(
            Ticket.id == ticket_id,
            Ticket.business_id == business_id
        )
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    ticket.status = "CLOSED"

    db.commit()
    db.refresh(ticket)

    return ticket


def get_open_tickets(
    db: Session,
    business_id: int
):
    validate_business(db, business_id)

    return (
        db.query(Ticket)
        .filter(
            Ticket.business_id == business_id,
            Ticket.status == "OPEN"
        )
        .all()
    )