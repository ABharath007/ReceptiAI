from app.database.database import engine
from app.database.base import Base

from app.models.business import Business
from app.models.service import Service
from app.models.resource import Resource
from app.models.business_settings import BusinessSettings

from app.models.customer import Customer

from app.models.resource_service import ResourceService
from app.models.resource_availability import ResourceAvailability
from app.models.resource_leave import ResourceLeave

from app.models.appointment import Appointment
from app.models.appointment_service import AppointmentService
from app.models.appointment_status_history import AppointmentStatusHistory

from app.models.ticket import Ticket

from app.models.knowledge_base import KnowledgeBase

from app.models.conversation_session import ConversationSession
from app.models.conversation_message import ConversationMessage
from app.models.conversation_summary import ConversationSummary


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")