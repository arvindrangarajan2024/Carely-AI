"""Support Ticket schemas for request/response validation"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class SupportTicketBase(BaseModel):
    """Base support ticket schema"""
    category: str = Field(..., min_length=1)
    subject: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10)
    language: str = "en"
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None


class SupportTicketCreate(SupportTicketBase):
    """Schema for creating a support ticket"""
    patient_id: Optional[int] = None
    priority: str = "medium"


class SupportTicketUpdate(BaseModel):
    """Schema for updating a support ticket"""
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    resolution_notes: Optional[str] = None


class SupportTicketResponse(SupportTicketBase):
    """Schema for support ticket response"""
    id: int
    ticket_number: str
    patient_id: Optional[int]
    priority: str
    status: str
    assigned_to: Optional[str]
    resolution_notes: Optional[str]
    resolved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


