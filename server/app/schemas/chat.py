"""Chat schemas"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ChatMessageRequest(BaseModel):
    """Chat message request schema"""
    message: str = Field(..., description="User message content", min_length=1, max_length=5000)
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID for continuing a conversation")


class ChatMessageResponse(BaseModel):
    """Chat message response schema"""
    response: str = Field(..., description="AI assistant response")
    message_id: str | None = Field(None, description="Optional message ID for tracking")
    conversation_id: str = Field(..., description="Conversation ID for this message")
    appointment_data: Optional[Dict[str, Any]] = Field(None, description="Appointment booking data if applicable")

