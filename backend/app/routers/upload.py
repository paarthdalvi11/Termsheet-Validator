from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.crud.chunk_ops import insert_pdf_chunks, get_chunks, update_chunk_vector
from app.models.documents import Document
from app.utils.rag.indexer import build_faiss_index
from app.utils.json_processor import process_json_data
from app.schemas import ChunkInput, DocumentIn
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(prefix="/upload", tags=["Upload"])

class ChunkModel(BaseModel):
    id: int = None
    document_id: int
    chunk_index: int
    content: str
    vector_id: str = None
    vector: List[float] = None

@router.post("/document")
async def upload_document(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a new document to the system
    """
    try:
        # Create document record
        db_document = Document(title=title)
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        # Return document info
        return {
            "status": "success",
            "document_id": db_document.id,
            "title": db_document.title
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Document upload failed: {str(e)}"
        )

@router.post("/chunks")
async def upload_json_chunks(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload document chunks from JSON file
    """
    try:
        # 1. Read and validate JSON
        contents = await file.read()
        chunks_data = json.loads(contents)
        
        # Validate structure
        if not isinstance(chunks_data, list) or not chunks_data:
            raise HTTPException(
                status_code=400,
                detail="Invalid JSON format: expected non-empty array of chunks"
            )
        
        # Check required fields
        for chunk in chunks_data:
            if not all(key in chunk for key in ["document_id", "chunk_index", "content"]):
                raise HTTPException(
                    status_code=400,
                    detail="Each chunk requires document_id, chunk_index, and content"
                )
        
        # Insert chunks with vector data if available
        inserted_chunks = insert_pdf_chunks(db, chunks_data)
        document_id = chunks_data[0]["document_id"]
        
        # Count chunks with vector data
        vector_count = sum(1 for chunk in chunks_data if "vector" in chunk and chunk["vector"])
        
        return {
            "status": "success",
            "document_id": document_id,
            "chunks_processed": len(inserted_chunks),
            "chunks_with_vectors": vector_count
        }
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON format in uploaded file"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )

@router.post("/upload-json-chunks")
async def upload_json_chunks_legacy(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Legacy endpoint for uploading document chunks from JSON file
    """
    # Redirect to the new endpoint with the same logic
    return await upload_json_chunks(file, db)

@router.post("/upload-json")
async def upload_json_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and process a complete JSON document
    """
    try:
        # Read JSON content
        content = await file.read()
        json_data = json.loads(content)
        
        # Extract document ID or generate one
        document_id = json_data.get("document_id")
        if not document_id:
            # Create document with provided or default title
            title = json_data.get("title", f"Document {datetime.now().isoformat()}")
            db_document = Document(title=title)
            db.add(db_document)
            db.commit()
            db.refresh(db_document)
            document_id = db_document.id
        
        # Process JSON into chunks
        chunks = process_json_data(json_data, document_id)
        
        # Store chunks in database
        db_chunks = insert_pdf_chunks(db, chunks)
        
        return {
            "status": "success",
            "document_id": document_id,
            "chunks_processed": len(db_chunks)
        }
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON format in uploaded file"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
      # Remove this extra curly brace

@router.post("/pdf")
async def upload_pdf(
    document_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Process and upload PDF file chunks
    """
    # Validate file is PDF
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    try:
        # Check document exists
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(
                status_code=404,
                detail=f"Document with ID {document_id} not found"
            )
        
        # Process PDF file and extract chunks
        contents = await file.read()
        
        # TODO: Implement PDF processing logic here
        # This would typically include:
        # 1. Extract text from PDF
        # 2. Split into chunks
        # 3. Generate embeddings
        # 4. Store chunks with document_id reference
        
        # For now, return placeholder
        return {
            "status": "success",
            "document_id": document_id,
            "message": "PDF processing functionality to be implemented"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF processing failed: {str(e)}"
        )

@router.put("/vectors/{document_id}")
async def generate_vectors(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Generate vector embeddings for all chunks of a specific document
    """
    try:
        # Check document exists
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(
                status_code=404,
                detail=f"Document with ID {document_id} not found"
            )
        
        # Get chunks for this document
        chunks = get_chunks(db, document_id=document_id)
        if not chunks:
            raise HTTPException(
                status_code=404,
                detail=f"No chunks found for document ID {document_id}"
            )
        
        # Process chunks and generate vectors
        updated_count = 0
        for chunk in chunks:
            if not chunk.vector:  # Only process chunks without vectors
                # Generate vector embedding for chunk content
                # This is a placeholder - implement your actual embedding logic
                vector_data = [0.0] * 768  # Example placeholder vector
                
                # Update chunk with vector data
                update_chunk_vector(db, chunk.id, vector_data)
                updated_count += 1
        
        return {
            "status": "success",
            "document_id": document_id,
            "chunks_updated": updated_count,
            "total_chunks": len(chunks)
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Vector generation failed: {str(e)}"
        )

@router.post("/build-index")
async def create_index(
    db: Session = Depends(get_db)
):
    """
    Build or rebuild the FAISS index from all available chunk vectors
    """
    try:
        # Get all chunks with vectors
        chunks = get_chunks(db)
        
        # Filter chunks that have vector data
        vector_chunks = [chunk for chunk in chunks if chunk.vector is not None]
        
        if not vector_chunks:
            raise HTTPException(
                status_code=404,
                detail="No chunks with vector data found to build index"
            )
        
        # Build FAISS index
        index_stats = build_faiss_index(vector_chunks)
        
        return {
            "status": "success",
            "chunks_indexed": len(vector_chunks),
            "index_stats": index_stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Index building failed: {str(e)}"
        )

class ChunkFilterParams(BaseModel):
    document_id: Optional[int] = None
    has_vector: Optional[bool] = None
    limit: Optional[int] = 100
    offset: Optional[int] = 0

@router.get("/chunks")
async def list_chunks(
    document_id: Optional[int] = None,
    has_vector: Optional[bool] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    List chunks with optional filtering
    """
    try:
        chunks = get_chunks(
            db, 
            document_id=document_id,
            has_vector=has_vector,
            limit=limit,
            offset=offset
        )
        
        return {
            "status": "success",
            "count": len(chunks),
            "chunks": [
                {
                    "id": chunk.id,
                    "document_id": chunk.document_id,
                    "chunk_index": chunk.chunk_index,
                    "content": chunk.content[:100] + "..." if chunk.content and len(chunk.content) > 100 else chunk.content,
                    "has_vector": chunk.vector is not None,
                    "vector_id": chunk.vector_id
                }
                for chunk in chunks
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving chunks: {str(e)}"
        )
