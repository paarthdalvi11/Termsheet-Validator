# app/models/extracted_data.py

from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class ExtractedData(Base):
    __tablename__ = "extracted_data"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, index=True)  # Foreign key to the documents table, if needed
    content = Column(Text)  # Example of extracted data, could be anything like text, numbers, etc.
