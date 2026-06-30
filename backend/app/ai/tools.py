from datetime import date, time

from langchain_core.tools import tool
from app.database.database import SessionLocal

from app.services.scheduling_service import get_available_slots
from app.services.booking_service import create_booking
from app.services.knowledge_service import (
    search_knowledge
)
from app.services.resource_service import (
    get_resources_by_service,
    get_services_by_resource,
    get_resource_by_name
)
from app.services.customer_service import (
    get_customer_by_phone,
    create_customer_if_not_exists
)
from app.services.ticket_service import (
    create_ticket,
    close_ticket as close_ticket_service,
    get_open_tickets
)


@tool
def search_business_knowledge(
    business_id: int,
    query: str
):
    """
    Search the business knowledge base using a customer query.
    """

    db = SessionLocal()

    try:
        return search_knowledge(
            db=db,
            business_id=business_id,
            query=query
        )
    finally:
        db.close()


@tool
def find_available_slots(
    resource_id: int,
    appointment_date: date
):
    """
Use this tool to retrieve all available appointment slots
for a specific resource on a given date.
"""

    db = SessionLocal()

    try:
        return get_available_slots(
            db=db,
            resource_id=resource_id,
            appointment_date=appointment_date
        )
    finally:
        db.close()


@tool
def book_appointment(
    business_id: int,
    customer_id: int,
    resource_id: int,
    appointment_date: date,
    start_time: time,
    end_time: time,
    special_notes: str | None = None
):
    """
Use this tool to book an appointment after verifying
that the requested slot is available.
"""
    db = SessionLocal()
    try:
        return create_booking(
            db=db,
            business_id=business_id,
            customer_id=customer_id,
            resource_id=resource_id,
            appointment_date=appointment_date,
            start_time=start_time,
            end_time=end_time,
            special_notes=special_notes
        )
    finally:
        db.close()


@tool
def find_resources_by_service(
    business_id: int,
    service_id: int
):
    """
    Find resources for a service.
    """
    db = SessionLocal()
    try:
        return get_resources_by_service(
            db=db,
            business_id=business_id,
            service_id=service_id
        )
    finally:
        db.close()


@tool
def find_services_by_resource(
    business_id: int,
    resource_id: int
):
    """
    Find services provided by a resource.
    """

    db = SessionLocal()

    try:
        return get_services_by_resource(
            db=db,
            business_id=business_id,
            resource_id=resource_id
        )
    finally:
        db.close()


@tool
def find_resource_by_name(
    business_id: int,
    resource_name: str
):
    """
    Find a resource using their name.
    """
    db = SessionLocal()
    try:
        return get_resource_by_name(
            db=db,
            business_id=business_id,
            resource_name=resource_name
        )
    finally:
        db.close()


@tool
def find_customer_by_phone(
    business_id: int,
    phone: str
):
    """
Retrieve a customer using their phone number.
Returns None if the customer does not exist.
"""
    db = SessionLocal()
    try:
        return get_customer_by_phone(
            db=db,
            business_id=business_id,
            phone=phone
        )
    finally:
        db.close()


@tool
def create_customer(
    business_id: int,
    name: str,
    phone: str,
    email: str | None = None
):
    """
    Register customer if they do not exist.
    """
    db = SessionLocal()
    try:
        return create_customer_if_not_exists(
            db=db,
            business_id=business_id,
            name=name,
            phone=phone,
            email=email
        )
    finally:
        db.close()


@tool
def raise_ticket(
    business_id: int,
    customer_id: int,
    subject: str,
    description: str,
    appointment_id: int | None = None,
    priority: str = "MEDIUM"
):
    """
Create a new support ticket for a customer.
Use this when the customer reports an issue or complaint.
"""
    db = SessionLocal()
    try:
        return create_ticket(
            db=db,
            business_id=business_id,
            customer_id=customer_id,
            subject=subject,
            description=description,
            appointment_id=appointment_id,
            priority=priority
        )
    finally:
        db.close()


@tool
def close_ticket(
    business_id: int,
    ticket_id: int
):
    """
    Close a ticket.
    """
    db = SessionLocal()
    try:
        return close_ticket_service(
            db=db,
            business_id=business_id,
            ticket_id=ticket_id
        )
    finally:
        db.close()


@tool
def list_open_tickets(
    business_id: int
):
    """
    Get all open tickets.
    """
    db = SessionLocal()
    try:
        return get_open_tickets(
            db=db,
            business_id=business_id
        )
    finally:
        db.close()