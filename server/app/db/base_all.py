"""Import all models for Alembic migrations"""
from app.db.base import Base  # noqa

# Import all models here so Alembic can detect them
from app.models.patient import Patient  # noqa
from app.models.appointment import Appointment  # noqa
from app.models.medical_record import MedicalRecord  # noqa
from app.models.support_ticket import SupportTicket  # noqa
from app.models.provider import Provider  # noqa
from app.models.chat_conversation import ChatConversation  # noqa
from app.models.chat_message import ChatMessage  # noqa




