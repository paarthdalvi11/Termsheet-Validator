from sqlalchemy import Column, Integer, String, Text, ForeignKey, ARRAY, Float
from sqlalchemy.orm import relationship
from app.database import Base

class PDFChunk(Base):
    __tablename__ = "pdf_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    vector = Column(ARRAY(Float), nullable=True)
    vector_id = Column(Integer, nullable=True)  # Changed from String to Integer

    # Relationship back to Document — match 'chunks'
    document = relationship("Document", back_populates="chunks")