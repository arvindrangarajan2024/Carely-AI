"""Patient schemas for request/response validation"""
from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional


class PatientBase(BaseModel):
    """Base patient schema"""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    phone_number: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    blood_type: Optional[str] = None
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None
    medications: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_policy_number: Optional[str] = None
    preferred_language: str = "en"


class PatientCreate(PatientBase):
    """Schema for creating a patient"""
    password: str = Field(..., min_length=8)


class PatientUpdate(BaseModel):
    """Schema for updating a patient"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None
    medications: Optional[str] = None
    preferred_language: Optional[str] = None


class PatientResponse(PatientBase):
    """Schema for patient response"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PatientLogin(BaseModel):
    """Schema for patient login"""
    email: EmailStr
    password: str


