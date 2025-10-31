"""Medical Record schemas for request/response validation"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class MedicalRecordBase(BaseModel):
    """Base medical record schema"""
    record_type: str = Field(..., min_length=1)
    record_date: datetime
    doctor_name: Optional[str] = None
    diagnosis: Optional[str] = None
    symptoms: Optional[str] = None
    treatment: Optional[str] = None
    medications_prescribed: Optional[str] = None
    lab_results: Optional[str] = None
    vital_signs: Optional[str] = None
    height_cm: Optional[float] = Field(None, ge=0, le=300)
    weight_kg: Optional[float] = Field(None, ge=0, le=500)
    blood_pressure: Optional[str] = None
    heart_rate: Optional[int] = Field(None, ge=30, le=250)
    temperature: Optional[float] = Field(None, ge=30.0, le=45.0)
    notes: Optional[str] = None
    follow_up_required: bool = False
    follow_up_date: Optional[datetime] = None


class MedicalRecordCreate(MedicalRecordBase):
    """Schema for creating a medical record"""
    patient_id: int


class MedicalRecordUpdate(BaseModel):
    """Schema for updating a medical record"""
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    medications_prescribed: Optional[str] = None
    notes: Optional[str] = None
    follow_up_required: Optional[bool] = None
    follow_up_date: Optional[datetime] = None


class MedicalRecordResponse(MedicalRecordBase):
    """Schema for medical record response"""
    id: int
    patient_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


