"""Health check endpoints"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Carely AI Healthcare Assistant API",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


