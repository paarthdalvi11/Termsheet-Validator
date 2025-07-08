from pydantic import BaseModel
from enum import Enum
from typing import List, Optional, Dict, Any

# Enum for severity levels
class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

# Schema for chunks
class ChunkInput(BaseModel):
    id: Optional[int] = None
    document_id: int
    chunk_index: int
    content: str
    vector_id: Optional[str] = None
    vector: Optional[List[float]] = None

# Schema for Document model
class DocumentIn(BaseModel):
    title: str
    content: Optional[str] = None
    author: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        orm_mode = True

# Schema for ExtractedData model
class ExtractedDataIn(BaseModel):
    document_id: int
    content: str
    extracted_at: Optional[str] = None

    class Config:
        orm_mode = True

# Schema for ValidationLog model
class ValidationLogIn(BaseModel):
    document_id: int
    status: str
    message: Optional[str] = None
    validated_at: Optional[str] = None

    class Config:
        orm_mode = True

# Schema for AuditTrail model
class AuditTrailIn(BaseModel):
    action: str
    document_id: int
    user_id: Optional[int] = None
    details: Optional[str] = None
    timestamp: Optional[str] = None

    class Config:
        orm_mode = True

# Schema for Validation Errors and Result
class ValidationError(BaseModel):
    type: str
    description: str
    section: str
    severity: Severity

class ClauseMatch(BaseModel):
    clause: str
    match_type: str  # 'match', 'partial', 'missing'
    similarity: float

# Schema for the final Validation Result
class ValidationResult(BaseModel):
    errors: List[ValidationError]
    criticality_score: int
    validation_summary: str
    clause_matches: List[ClauseMatch] = []

class SimpleValidationResult(BaseModel):
    is_valid: bool
    message: str

class AuditLog(BaseModel):
    validation_id: int
    action: str
    timestamp: str
    user_id: str