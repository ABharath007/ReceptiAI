from langchain_core.messages import HumanMessage, AIMessage
from sqlalchemy.orm import Session

from app.ai.graph import reception_graph
from app.ai.context import AgentContext
from app.ai.context_manager import set_context, reset_context

from app.models.conversation_session import ConversationSession
from app.models.conversation_message import ConversationMessage

from app.services.conversation_service import (
    create_session,
    add_message,
)


def invoke_agent(
    message: str,
    business_id: int,
    db: Session,
    session_id: int | None = None
):
    session = None
    history = []

    # ---------------------------------------------------------
    # Load existing conversation session and history
    # ---------------------------------------------------------

    if session_id:

        session = (
            db.query(ConversationSession)
            .filter(
                ConversationSession.id == session_id,
                ConversationSession.business_id == business_id
            )
            .first()
        )

        if not session:
            raise ValueError("Conversation session not found")

        history = (
            db.query(ConversationMessage)
            .filter(
                ConversationMessage.session_id == session_id
            )
            .order_by(
                ConversationMessage.created_at.asc()
            )
            .all()
        )

    # ---------------------------------------------------------
    # Create agent context
    # ---------------------------------------------------------

    context = AgentContext(
        db=db,
        business_id=business_id,
        customer_id=session.customer_id if session else None,
        session_id=session.id if session else None
    )

    context_token = set_context(context)

    try:

        # -----------------------------------------------------
        # Convert database conversation history into
        # LangChain messages
        # -----------------------------------------------------

        messages = []

        for item in history:

            if item.sender == "user":

                messages.append(
                    HumanMessage(
                        content=item.message
                    )
                )

            elif item.sender == "assistant":

                messages.append(
                    AIMessage(
                        content=item.message
                    )
                )

        # -----------------------------------------------------
        # Add current user message
        # -----------------------------------------------------

        messages.append(
            HumanMessage(
                content=message
            )
        )

        # -----------------------------------------------------
        # Create graph state
        # -----------------------------------------------------

        state = {
            "messages": messages,
            "business_id": business_id,
            "customer_id": context.customer_id,
            "customer_phone": context.customer_phone,
            "intent": None,
            "resource_id": None,
            "service_id": None,
            "appointment_date": None,
            "available_slots": None,
            "ticket_id": None,
            "session_id": context.session_id,
            "response": None
        }

        print("Agent context created:")
        print(context)

        print("Conversation history:")
        print(history)

        print("Before graph")

        # -----------------------------------------------------
        # Run LangGraph
        # -----------------------------------------------------

        result = reception_graph.invoke(state)

        print("After graph")
        print(result)

        # -----------------------------------------------------
        # Get final AI response
        # -----------------------------------------------------

        response = result["messages"][-1].content

        # -----------------------------------------------------
        # Create a new session if this is the first message
        # and the customer was identified during the agent run
        # -----------------------------------------------------

        if (
            context.session_id is None
            and context.customer_id is not None
        ):

            session = create_session(
                db=db,
                business_id=business_id,
                customer_id=context.customer_id
            )

            context.session_id = session.id

        # -----------------------------------------------------
        # Save current conversation messages
        # -----------------------------------------------------

        if context.session_id is not None:

            add_message(
                db=db,
                session_id=context.session_id,
                sender="user",
                message=message
            )

            add_message(
                db=db,
                session_id=context.session_id,
                sender="assistant",
                message=response
            )

        # -----------------------------------------------------
        # Return response + session ID
        # -----------------------------------------------------

        return {
            "response": response,
            "session_id": context.session_id
        }

    finally:

        # Always clear ContextVar
        reset_context(context_token)