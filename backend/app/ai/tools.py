import re
from datetime import date, time
import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from langchain_core.tools import tool

from app.ai.context_manager import get_context

from app.ai.tool_results import (
    tool_success,
    tool_failure,
    serialize_resource,
    serialize_service,
    serialize_customer,
    serialize_appointment,
    serialize_ticket,
    serialize_knowledge,
)

from app.services.scheduling_service import get_available_slots
from app.services.booking_service import create_booking
from app.services.knowledge_service import search_knowledge
from app.services.service_service import get_service_by_name

from app.services.resource_service import (
    get_resources_by_service,
    get_services_by_resource,
    get_resource_by_name,
)

from app.services.customer_service import (
    get_customer_by_phone,
    create_customer_if_not_exists,
)

from app.services.ticket_service import (
    create_ticket,
    close_ticket as close_ticket_service,
    get_open_tickets,
)


logger = logging.getLogger(__name__)


# ============================================================
# COMMON ERROR HANDLER
# ============================================================

def _handle_tool_error(context, exc: Exception):
    """
    Convert service/database exceptions into a safe structured
    response for the LLM.
    """

    if isinstance(exc, HTTPException):
        return tool_failure(
            message=str(exc.detail)
        )

    if isinstance(exc, SQLAlchemyError):
        context.db.rollback()

        logger.exception(
            "Database error while executing AI tool"
        )

        return tool_failure(
            message="A database error occurred while processing the request."
        )

    context.db.rollback()

    logger.exception(
        "Unexpected error while executing AI tool"
    )

    return tool_failure(
        message="An unexpected error occurred while processing the request."
    )


# ============================================================
# KNOWLEDGE
# ============================================================

@tool
def search_business_knowledge(query: str):
    """
    Search the current business knowledge base using a customer query.

    The business ID and database session come from the trusted
    agent context.
    """

    context = get_context()

    print("Searching knowledge")
    print("Business ID:", context.business_id)
    print("Query:", query)

    try:
        results = search_knowledge(
            db=context.db,
            business_id=context.business_id,
            query=query,
        )

        if not results:
            return tool_success(
                message="No relevant business information was found.",
                data={
                    "results": []
                },
            )

        return tool_success(
            message=f"Found {len(results)} relevant knowledge item(s).",
            data={
                "results": [
                    serialize_knowledge(item)
                    for item in results
                ]
            },
        )

    except Exception as exc:
        return _handle_tool_error(context, exc)


# ============================================================
# SCHEDULING
# ============================================================

@tool
def find_available_slots(
    resource_id: int,
    service_id: int,
    appointment_date: date,
    
):
    """
    Retrieve all available appointment start times for a resource
    on a specific date.

    The business context comes from the trusted agent context.
    """

    context = get_context()

    print("Finding available slots")
    print("Business ID:", context.business_id)
    print("Resource ID:", resource_id)
    print("Date:", appointment_date)

    try:
        slots = get_available_slots(
            db=context.db,
            resource_id=resource_id,
            service_id=service_id,
            appointment_date=appointment_date,
        )

        if not slots:
            return tool_success(
                message=(
                    f"No available slots found for resource "
                    f"{resource_id} on {appointment_date}."
                ),
                data={
                    "resource_id": resource_id,
                    "service_id": service_id,
                    "appointment_date": str(appointment_date),
                    "available": False,
                    "slots": [],
                },
            )

        return tool_success(
            message=f"Available slots found for {appointment_date}.",
            data={
                "resource_id": resource_id,
                "service_id": service_id,
                "appointment_date": str(appointment_date),
                "available": True,
                "slots": [
                    str(slot)
                    for slot in slots
                ],
            },
        )

    except Exception as exc:
        return _handle_tool_error(context, exc)


# ============================================================
# BOOKING
# ============================================================

def parse_time_input(value: str) -> time:
    if not value or not value.strip():
        raise ValueError("Time cannot be empty.")

    text = value.strip().lower()

    # Normalize common expressions
    text = text.replace("’", "'")
    text = text.replace("o'clock", "")
    text = text.replace("oclock", "")
    text = text.replace("in the morning", "am")
    text = text.replace("in the afternoon", "pm")
    text = text.replace("in the evening", "pm")
    text = text.replace("in the night", "pm")

    text = re.sub(r"\s+", " ", text).strip()

    # 10 am / 10 pm
    match = re.fullmatch(r"(\d{1,2})\s*(am|pm)", text)

    if match:
        hour = int(match.group(1))
        period = match.group(2)

        if hour < 1 or hour > 12:
            raise ValueError("Invalid hour.")

        if period == "am":
            hour = 0 if hour == 12 else hour
        else:
            hour = 12 if hour == 12 else hour + 12

        return time(hour, 0)

    # 10:00 am / 10:00 pm
    # 10:00:00 am / 10:00:00 pm
    match = re.fullmatch(
        r"(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(am|pm)",
        text
    )

    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        second = int(match.group(3) or 0)
        period = match.group(4)

        if hour < 1 or hour > 12:
            raise ValueError("Invalid hour.")

        if minute > 59 or second > 59:
            raise ValueError("Invalid minute or second.")

        if period == "am":
            hour = 0 if hour == 12 else hour
        else:
            hour = 12 if hour == 12 else hour + 12

        return time(hour, minute, second)

    # 10:00 / 10:00:00 / 9:30
    match = re.fullmatch(
        r"(\d{1,2}):(\d{2})(?::(\d{2}))?",
        text
    )

    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        second = int(match.group(3) or 0)

        if hour > 23 or minute > 59 or second > 59:
            raise ValueError("Invalid time.")

        return time(hour, minute, second)

    # 10 / 9
    match = re.fullmatch(r"(\d{1,2})", text)

    if match:
        hour = int(match.group(1))

        if hour > 23:
            raise ValueError("Invalid hour.")

        return time(hour, 0)

    raise ValueError(
        "Invalid time format. Please provide a time such as 10 AM or 10:00."
    )


@tool
def book_appointment(
    resource_id: int,
    appointment_date: date,
    start_time: str,
    service_id: int,
    special_notes: str | None = None,
):
    """
    Book an appointment for the current customer.

    The business ID, customer ID, and database session come
    from the trusted agent context.
    """

    context = get_context()

    if context.customer_id is None:
        return tool_failure(
            message="The customer has not been identified yet."
        )
        
    try:
        parsed_start_time = parse_time_input(start_time)

    except ValueError as exc:
        return tool_failure(
            message=str(exc),
            data={
                "start_time": start_time
            }
        )

    print("Booking appointment")
    print("Business ID:", context.business_id)
    print("Customer ID:", context.customer_id)
    print("Resource ID:", resource_id)
    print("Date:", appointment_date)
    print("Start:", parsed_start_time)

    try:
        appointment = create_booking(
            db=context.db,
            business_id=context.business_id,
            customer_id=context.customer_id,
            resource_id=resource_id,
            service_id=service_id,
            appointment_date=appointment_date,
            start_time=parsed_start_time,
            special_notes=special_notes,
        )

        return tool_success(
            message="Appointment booked successfully.",
            data=serialize_appointment(appointment),
        )

    except Exception as exc:
        return _handle_tool_error(context, exc)


# ============================================================
# RESOURCE / SERVICE
# ============================================================

@tool
def find_resources_by_service(
    service_id: int,
):
    """
    Find resources that provide a specific service.
    """

    context = get_context()

    print("Finding resources for service")
    print("Business ID:", context.business_id)
    print("Service ID:", service_id)

    try:
        resources = get_resources_by_service(
            db=context.db,
            business_id=context.business_id,
            service_id=service_id,
        )

        if not resources:
            return tool_success(
                message=f"No resources found for service {service_id}.",
                data={
                    "service_id": service_id,
                    "resources": [],
                },
            )

        return tool_success(
            message=f"Found {len(resources)} resource(s).",
            data={
                "service_id": service_id,
                "resources": [
                    serialize_resource(resource)
                    for resource in resources
                ],
            },
        )

    except Exception as exc:
        return _handle_tool_error(context, exc)


@tool
def find_services_by_resource(
    resource_id: int,
):
    """
    Find services provided by a specific resource.
    """

    context = get_context()

    print("Finding services for resource")
    print("Business ID:", context.business_id)
    print("Resource ID:", resource_id)

    try:
        services = get_services_by_resource(
            db=context.db,
            business_id=context.business_id,
            resource_id=resource_id,
        )

        if not services:
            return tool_success(
                message=f"No services found for resource {resource_id}.",
                data={
                    "resource_id": resource_id,
                    "services": [],
                },
            )

        return tool_success(
            message=f"Found {len(services)} service(s).",
            data={
                "resource_id": resource_id,
                "services": [
                    serialize_service(service)
                    for service in services
                ],
            },
        )

    except Exception as exc:
        return _handle_tool_error(context, exc)


@tool
def find_resource_by_name(
    resource_name: str,
):
    """
    Find a resource such as a doctor, stylist, therapist,
    or staff member by name for the current business.

    The business ID and database session come from the
    trusted agent context.
    """

    context = get_context()

    print("Finding resource")
    print("Business ID:", context.business_id)
    print("Resource name:", resource_name)

    try:
        resource = get_resource_by_name(
            db=context.db,
            business_id=context.business_id,
            resource_name=resource_name,
        )

        return tool_success(
            message=f"Resource '{resource_name}' found.",
            data=serialize_resource(resource),
        )

    except Exception as exc:
        if isinstance(exc, HTTPException) and exc.status_code == 404:
            return tool_failure(
                message=f"No resource named '{resource_name}' was found.",
                data=None,
            )

        return _handle_tool_error(context, exc)

@tool
def find_service_by_name(
    service_name: str,
):
    """
    Find an active service by name for the current business.
    """

    context = get_context()

    print("Finding service")
    print("Business ID:", context.business_id)
    print("Service name:", service_name)

    try:
        service = get_service_by_name(
            db=context.db,
            business_id=context.business_id,
            service_name=service_name,
        )

        return tool_success(
            message=f"Service '{service_name}' found.",
            data=serialize_service(service),
        )

    except Exception as exc:
        if isinstance(exc, HTTPException) and exc.status_code == 404:
            return tool_failure(
                message=f"No service named '{service_name}' was found.",
                data=None,
            )

        return _handle_tool_error(context, exc)

# ============================================================
# CUSTOMER
# ============================================================

@tool
def find_customer_by_phone(
    phone: str,
):
    """
    Find a customer using their phone number for the current business.

    If the customer does not exist, the tool returns a structured
    response instead of returning None.
    """

    context = get_context()

    print("Finding customer")
    print("Business ID:", context.business_id)
    print("Phone:", phone)

    try:
        customer = get_customer_by_phone(
            db=context.db,
            business_id=context.business_id,
            phone=phone,
        )

        if customer is None:
            return tool_failure(
                message="No customer was found with that phone number.",
                data=None,
            )

        context.customer_id = customer.id
        context.customer_phone = phone

        print("Customer found:", customer.id)

        return tool_success(
            message="Customer found.",
            data=serialize_customer(customer),
        )

    except Exception as exc:
        return _handle_tool_error(context, exc)


@tool
def create_customer(
    name: str,
    phone: str,
    email: str | None = None,
):
    """
    Create a customer for the current business if the customer
    does not already exist.
    """

    context = get_context()

    print("Creating/finding customer")
    print("Business ID:", context.business_id)
    print("Phone:", phone)

    try:
        customer = create_customer_if_not_exists(
            db=context.db,
            business_id=context.business_id,
            name=name,
            phone=phone,
            email=email,
        )

        context.customer_id = customer.id
        context.customer_phone = phone

        print("Customer ID:", customer.id)

        return tool_success(
            message="Customer is ready for the appointment.",
            data=serialize_customer(customer),
        )

    except Exception as exc:
        return _handle_tool_error(context, exc)


# ============================================================
# TICKETS
# ============================================================

@tool
def raise_ticket(
    subject: str,
    description: str,
    appointment_id: int | None = None,
    priority: str = "MEDIUM",
):
    """
    Create a support ticket for the current customer.

    The business ID, customer ID, and database session come
    from the trusted agent context.
    """

    context = get_context()

    if context.customer_id is None:
        return tool_failure(
            message="The customer has not been identified yet."
        )

    print("Creating ticket")
    print("Business ID:", context.business_id)
    print("Customer ID:", context.customer_id)

    try:
        ticket = create_ticket(
            db=context.db,
            business_id=context.business_id,
            customer_id=context.customer_id,
            subject=subject,
            description=description,
            appointment_id=appointment_id,
            priority=priority,
        )

        return tool_success(
            message="Support ticket created successfully.",
            data=serialize_ticket(ticket),
        )

    except Exception as exc:
        return _handle_tool_error(context, exc)


@tool
def close_ticket(
    ticket_id: int,
):
    """
    Close a ticket belonging to the current business.
    """

    context = get_context()

    print("Closing ticket")
    print("Business ID:", context.business_id)
    print("Ticket ID:", ticket_id)

    try:
        ticket = close_ticket_service(
            db=context.db,
            business_id=context.business_id,
            ticket_id=ticket_id,
        )

        return tool_success(
            message="Ticket closed successfully.",
            data=serialize_ticket(ticket),
        )

    except Exception as exc:
        return _handle_tool_error(context, exc)


@tool
def list_open_tickets():
    """
    Get all open tickets for the current business.
    """

    context = get_context()

    print("Getting open tickets")
    print("Business ID:", context.business_id)

    try:
        tickets = get_open_tickets(
            db=context.db,
            business_id=context.business_id,
        )

        if not tickets:
            return tool_success(
                message="There are no open tickets.",
                data={
                    "tickets": []
                },
            )

        return tool_success(
            message=f"Found {len(tickets)} open ticket(s).",
            data={
                "tickets": [
                    serialize_ticket(ticket)
                    for ticket in tickets
                ]
            },
        )

    except Exception as exc:
        return _handle_tool_error(context, exc)