from fastapi import APIRouter
from app.database import database
from app.models import documents, extracted_data, validation_logs, audit_trail
from app.schemas import DocumentIn, ExtractedDataIn, ValidationLogIn, AuditTrailIn
from app.utils.rag.chatbot.indexer import build_chatbot_index

router = APIRouter()

@router.post("/upload")
async def upload_doc(payload: DocumentIn):
    query = documents.insert().values(
        name=payload.name,
        uploaded_by=payload.uploaded_by
    )
    doc_id = await database.execute(query)
    return {"message": "Document uploaded", "document_id": doc_id}

@router.post("/extracted_data")
async def insert_extracted(payload: ExtractedDataIn):
    query = extracted_data.insert().values(**payload.dict())
    await database.execute(query)
    return {"message": "Extracted data inserted"}

# @router.post("/validate_log")
# async def log_validation(payload: ValidationLogIn):
#     query = validation_logs.insert().values(
#         **payload.dict(),
#         checked_at=datetime.utcnow()
#     )
#     await database.execute(query)
#     return {"message": "Validation log inserted"}

# @router.post("/audit")
# async def add_audit_log(payload: AuditTrailIn):
#     query = audit_trail.insert().values(
#         **payload.dict(),
#         timestamp=datetime.utcnow()
#     )
#     await database.execute(query)
#     return {"message": "Audit log added"}

@router.post("/build-chatbot-index")
def create_chatbot_index():
    """Build or rebuild the unified FAISS index for the chatbot"""
    try:
        result = build_chatbot_index()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
