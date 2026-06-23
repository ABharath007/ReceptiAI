from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.ticket import Ticket
from app.models.business import Business
from app.models.customer import Customer
from app.models.appointment import Appointment

from app.schemas.ticket import (
    TicketCreate,
    TicketUpdate,
    TicketResponse
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post(
    "/",
    response_model=TicketResponse
)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db)
):

    business = db.query(Business).filter(
        Business.id == ticket.business_id
    ).first()

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    customer = db.query(Customer).filter(
        Customer.id == ticket.customer_id,
        Customer.business_id == ticket.business_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if ticket.appointment_id:

        appointment = db.query(Appointment).filter(
            Appointment.id == ticket.appointment_id
        ).first()

        if not appointment:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found"
            )

    new_ticket = Ticket(
        business_id=ticket.business_id,
        customer_id=ticket.customer_id,
        appointment_id=ticket.appointment_id,
        subject=ticket.subject,
        description=ticket.description,
        status="OPEN",
        priority=ticket.priority
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


@router.get(
    "/",
    response_model=list[TicketResponse]
)
def get_tickets(
    db: Session = Depends(get_db)
):
    return db.query(Ticket).all()


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse
)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return ticket


@router.put(
    "/{ticket_id}",
    response_model=TicketResponse
)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db)
):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    ticket.business_id = ticket_data.business_id
    ticket.customer_id = ticket_data.customer_id
    ticket.appointment_id = ticket_data.appointment_id
    ticket.subject = ticket_data.subject
    ticket.description = ticket_data.description
    ticket.status = ticket_data.status
    ticket.priority = ticket_data.priority

    db.commit()
    db.refresh(ticket)

    return ticket


@router.delete(
    "/{ticket_id}"
)
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    db.delete(ticket)
    db.commit()

    return {
        "message": "Ticket deleted successfully"
    }