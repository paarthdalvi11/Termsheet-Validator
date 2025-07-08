# app/crud/operations.py  (or chunk_ops.py, wherever you define insert_pdf_chunks)

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.pdf_chunk import PDFChunk
# Import the model that actually maps to your parent table:
# — If your foreign‑key is pdf_chunks.document_id → pdf_documents.id,
#   import the PDFDocument model (not Document).
from app.models.documents import Document  

def insert_pdf_chunks(db: Session, chunks: list[dict]):
    try:
        # 1️⃣ All chunks must share the same document_id
        doc_ids = {c["document_id"] for c in chunks}
        if len(doc_ids) != 1:
            raise ValueError("All chunks must share the same document_id")
        document_id = doc_ids.pop()

        # 2️⃣ Ensure the parent row exists (auto-create if missing)
        parent = db.query(Document).filter(Document.id == document_id).first()
        if not parent:
            parent = Document(id=document_id, title=f"Document {document_id}")
            db.add(parent)
            # db.flush() pushes the INSERT but does not commit
            db.flush()

        # 3️⃣ Now insert your chunks
        db_objs = []
        for ch in chunks:
            db_chunk = PDFChunk(
                document_id=ch["document_id"],
                chunk_index=ch["chunk_index"],
                content=ch["content"],
                vector=ch["vector"],
                vector_id=ch.get("vector_id")
            )
            db.add(db_chunk)
            db_objs.append(db_chunk)

        # 4️⃣ Commit everything
        db.commit()
        return db_objs

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Chunk insertion failed: {e}")
