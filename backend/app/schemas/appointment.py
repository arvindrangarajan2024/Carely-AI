"""Appointment schemas for request/response validation"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AppointmentBase(BaseModel):
    """Base appointment schema"""
    doctor_name: str = Field(..., min_length=1)
    appointment_type: str = Field(..., min_length=1)
    scheduled_time: datetime
    duration_minutes: int = Field(default=30, ge=15, le=240)
    reason: Optional[str] = None
    notes: Optional[str] = None
    location: Optional[str] = None
    is_virtual: bool = False


class AppointmentCreate(AppointmentBase):
    """Schema for creating an appointment"""
    patient_id: int


class AppointmentUpdate(BaseModel):
    """Schema for updating an appointment"""
    scheduled_time: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=15, le=240)
    status: Optional[str] = None
    notes: Optional[str] = None
    is_virtual: Optional[bool] = None


class AppointmentResponse(AppointmentBase):
    """Schema for appointment response"""
    id: int
    patient_id: int
    status: str
    reminder_sent: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

