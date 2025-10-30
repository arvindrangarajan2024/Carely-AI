"""Medical Record database model"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from datetime import datetime
from app.db.base import Base


class MedicalRecord(Base):
    """Medical Record model"""
    __tablename__ = "medical_records"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    record_type = Column(String, nullable=False)  # diagnosis, lab_result, prescription, etc.
    record_date = Column(DateTime, nullable=False)
    doctor_name = Column(String)
    diagnosis = Column(Text)
    symptoms = Column(Text)
    treatment = Column(Text)
    medications_prescribed = Column(Text)
    lab_results = Column(Text)
    vital_signs = Column(Text)  # JSON string of vital signs
    height_cm = Column(Float)
    weight_kg = Column(Float)
    blood_pressure = Column(String)
    heart_rate = Column(Integer)
    temperature = Column(Float)
    notes = Column(Text)
    follow_up_required = Column(Integer, default=0)
    follow_up_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


