"""Patient database model"""
from sqlalchemy import Column, Integer, String, DateTime, Date, Text
from datetime import datetime
from app.db.base import Base


class Patient(Base):
    """Patient model"""
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    phone_number = Column(String)
    address = Column(Text)
    emergency_contact_name = Column(String)
    emergency_contact_phone = Column(String)
    blood_type = Column(String)
    allergies = Column(Text)
    medical_conditions = Column(Text)
    medications = Column(Text)
    insurance_provider = Column(String)
    insurance_policy_number = Column(String)
    preferred_language = Column(String, default="en")
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

