"""API v1 router aggregation"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    patients,
    medical_records,
    support_tickets,
    health,
    chat
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(patients.router, prefix="/patients", tags=["Patients"])
api_router.include_router(medical_records.router, prefix="/medical-records", tags=["Medical Records"])
api_router.include_router(support_tickets.router, prefix="/support-tickets", tags=["Support Tickets"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])

# Note: Appointment management is now handled through the AI Chat Agent
# All appointment operations (create, list, cancel, update) are available via /chat endpoint


