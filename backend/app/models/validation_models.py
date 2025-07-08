from pydantic import BaseModel
from typing import List, Optional
from app.database import Base
from sqlalchemy import Column, Integer, String


class ValidationError(BaseModel):
    type: str
    description: str
    section: str
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"

class ValidationModel(Base):
    __tablename__ = "validation_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)


class ValidationResult(BaseModel):
    errors: List[ValidationError]
    criticality_score: int
    validation_summary: str
    document_hash: str

class AuditLog(BaseModel):
    validation_id: int
    action: str
    timestamp: str
    user_id: str