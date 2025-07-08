from sqlalchemy import Column, Integer, String, DateTime, Text
from app.models.base import Base
from datetime import datetime

class ValidationLog(Base):
    __tablename__ = "validation_logs"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, index=True)  # Foreign key to documents
    status = Column(String)  # Example: "valid" or "invalid"
    message = Column(Text, nullable=True)  # Example message explaining the validation result
    created_at = Column(DateTime, default=datetime.utcnow)