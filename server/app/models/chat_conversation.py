"""Chat conversation database model"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base
import uuid


def generate_conversation_id():
    """Generate a unique conversation ID"""
    return str(uuid.uuid4())


class ChatConversation(Base):
    """Chat conversation model - represents a conversation session"""
    __tablename__ = "chat_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, unique=True, index=True, nullable=False, default=generate_conversation_id)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    title = Column(String, nullable=True)  # Optional title/summary of conversation
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

