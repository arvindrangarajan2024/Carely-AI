"""Chat message database model"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base


class ChatMessage(Base):
    """Chat message model - stores individual messages in a conversation"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, ForeignKey("chat_conversations.conversation_id"), nullable=False, index=True)
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    message_id = Column(String, nullable=True)  # Optional message ID for tracking
    created_at = Column(DateTime, default=datetime.utcnow)

