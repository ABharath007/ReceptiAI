from typing import Any


def tool_success(
    message: str,
    data: Any = None
) -> dict:
    return {
        "success": True,
        "message": message,
        "data": data
    }


def tool_failure(
    message: str,
    data: Any = None
) -> dict:
    return {
        "success": False,
        "message": message,
        "data": data
    }


def serialize_resource(resource) -> dict:
    return {
        "resource_id": resource.id,
        "name": resource.name,
        "resource_type": resource.resource_type,
        "bio": resource.bio,
        "experience_years": resource.experience_years,
        "is_active": resource.is_active
    }


def serialize_service(service) -> dict:
    return {
        "service_id": service.id,
        "name": service.name,
        "description": service.description,
        "duration_minutes": service.duration_minutes,
        "price": service.price,
        "is_active": service.is_active
    }


def serialize_customer(customer) -> dict:
    return {
        "customer_id": customer.id,
        "name": customer.name,
        "phone": customer.phone,
        "email": customer.email
    }


def serialize_appointment(appointment) -> dict:
    return {
        "appointment_id": appointment.id,
        "business_id": appointment.business_id,
        "customer_id": appointment.customer_id,
        "resource_id": appointment.resource_id,
        "appointment_date": str(appointment.appointment_date),
        "start_time": str(appointment.start_time),
        "end_time": str(appointment.end_time),
        "status": appointment.status,
        "special_notes": appointment.special_notes
    }


def serialize_ticket(ticket) -> dict:
    return {
        "ticket_id": ticket.id,
        "customer_id": ticket.customer_id,
        "appointment_id": ticket.appointment_id,
        "subject": ticket.subject,
        "description": ticket.description,
        "status": ticket.status,
        "priority": ticket.priority
    }


def serialize_knowledge(knowledge) -> dict:
    return {
        "knowledge_id": knowledge.id,
        "category": knowledge.category,
        "title": knowledge.title,
        "content": knowledge.content
    }