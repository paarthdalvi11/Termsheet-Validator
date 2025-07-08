# app/models/audit_trail.py

from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class AuditTrail(Base):
    __tablename__ = "audit_trail"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)  # Assuming you have a user system in place
    action = Column(String)  # The action performed, e.g., "update", "delete"
    details = Column(String)  # Details about the action performed
    timestamp = Column(DateTime, default=datetime.utcnow)
