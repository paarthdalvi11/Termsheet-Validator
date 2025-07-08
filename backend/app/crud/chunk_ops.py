from sqlalchemy.orm import Session
from app.models.pdf_chunk import PDFChunk
from app.models.documents import Document
from fastapi import HTTPException
import numpy as np

def insert_pdf_chunks(db: Session, chunks: list[dict]):
    """Handle batch insertion of chunks with validation"""
    try:
        # Validate all chunks belong to same document
        document_ids = {chunk["document_id"] for chunk in chunks}
        if len(document_ids) != 1:
            raise ValueError("All chunks must belong to the same document")
        
        document_id = document_ids.pop()
        
        # Verify document exists
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            # Create document if it doesn't exist
            document = Document(id=document_id, title=f"Document {document_id}")
            db.add(document)
            db.flush()
        
        # Prepare chunks
        db_chunks = []
        for chunk in chunks:
            db_chunk = PDFChunk(
                document_id=chunk["document_id"],
                chunk_index=chunk["chunk_index"],
                content=chunk["content"],
                # Include vector data if present
                vector=chunk.get("vector")
            )
            db.add(db_chunk)
            db_chunks.append(db_chunk)
        
        db.commit()
        return db_chunks
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Chunk insertion failed: {str(e)}"
        )

def get_chunks(db: Session, document_id: int):
    """Retrieve chunks ordered by index"""
    return (
        db.query(PDFChunk)
        .filter(PDFChunk.document_id == document_id)
        .order_by(PDFChunk.chunk_index)
        .all()
    )

def update_chunk_vector(db: Session, chunk_id: int, vector: list[float]):
    """Update chunk with vector data"""
    try:
        db_chunk = db.query(PDFChunk).get(chunk_id)
        if not db_chunk:
            raise ValueError(f"Chunk {chunk_id} not found")
        
        db_chunk.vector = vector  # Changed from embedding to vector
        db_chunk.vector_id = str(chunk_id)  # Use chunk ID as vector_id
        db.commit()
        return db_chunk
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Vector update failed: {str(e)}"  # Updated error message
        )
def get_all_chunks(db: Session):
    """Get all chunks across all documents with vector embeddings"""
    return db.query(PDFChunk).filter(PDFChunk.vector.isnot(None)).all()

def get_chunks_by_ids(db: Session, chunk_ids: list[int]):
    """Get chunks by their IDs"""
    return db.query(PDFChunk).filter(PDFChunk.id.in_(chunk_ids)).all()
