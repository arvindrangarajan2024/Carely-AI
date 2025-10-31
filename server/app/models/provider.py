"""Provider database model"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.db.base import Base


class Provider(Base):
    """Provider model"""
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone_number = Column(String)
    specialty = Column(String)
    address = Column(Text)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



