"""Database base configuration"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Note: Models will be imported automatically when needed
# Do not import models here to avoid circular imports

