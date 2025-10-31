"""Support Ticket database model"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from app.db.base import Base


class SupportTicket(Base):
    """Support Ticket model for multilingual support routing"""
    __tablename__ = "support_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True, index=True)
    ticket_number = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, nullable=False)  # appointment, billing, technical, medical_inquiry, etc.
    priority = Column(String, default="medium")  # low, medium, high, urgent
    status = Column(String, default="open")  # open, in_progress, resolved, closed
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    language = Column(String, default="en")  # Language of the ticket
    assigned_to = Column(String)  # Agent/department assigned to
    contact_email = Column(String)
    contact_phone = Column(String)
    resolution_notes = Column(Text)
    resolved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


