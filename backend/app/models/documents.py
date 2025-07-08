from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # Make sure this line has the same indentation as the other attributes
    chunks = relationship("PDFChunk", back_populates="document")