from typing import TypedDict, Optional, List
from langchain_core.messages import BaseMessage


class ReceptionState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    # Incoming user message
    message: List[BaseMessage]

    # Business context
    business_id: int

    # Customer information
    customer_id: Optional[int]
    customer_phone: Optional[str]

    # Intent detected by AI
    intent: Optional[str]

    # Resource information
    resource_id: Optional[int]

    # Service information
    service_id: Optional[int]

    # Appointment information
    appointment_date: Optional[str]
    available_slots: Optional[List[str]]

    # Ticket
    ticket_id: Optional[int]

    # Conversation
    session_id: Optional[int]

    # Final AI response
    response: Optional[str]