"""Appointment database model"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from app.db.base import Base


class Appointment(Base):
    """Appointment model"""
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    doctor_name = Column(String, nullable=False)
    appointment_type = Column(String, nullable=False)  # consultation, follow-up, emergency, etc.
    scheduled_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=30)
    status = Column(String, default="scheduled")  # scheduled, confirmed, completed, cancelled
    reason = Column(Text)
    notes = Column(Text)
    location = Column(String)
    is_virtual = Column(Integer, default=0)  # 0 for in-person, 1 for virtual
    reminder_sent = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

