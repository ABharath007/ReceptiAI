from typing import TypedDict, Optional, List, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class ReceptionState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    # Incoming user message
    messages: Annotated[List[BaseMessage], add_messages]

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