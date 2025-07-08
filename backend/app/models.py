from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class DocumentChunk(Base):
    __tablename__ = 'document_chunks'

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    chunk_index = Column(Integer)
    content = Column(String)
    vector_id = Column(Integer, nullable=True)

    document = relationship("Document", back_populates="chunks")