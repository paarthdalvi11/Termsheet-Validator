from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.utils.validation_helpers import rule_based_checks
from app.utils.llm_integration import LLMValidator
from app.schemas import ValidationResult, ValidationError
from app.crud.validation_ops import ValidationOperations
import hashlib

router = APIRouter(prefix="/analyze", tags=["Analysis"])

@router.post("/document", response_model=ValidationResult)
async def analyze_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Analyze uploaded document for compliance and validation issues
    """
    # Read file contents
    file_contents = await file.read()
    
    # Create file hash for tracking
    file_hash = hashlib.md5(file_contents).hexdigest()
    
    try:
        # Convert to text based on file type
        from app.utils.ocr import extract_text_from_file
        file.file.seek(0)  # Reset file pointer
        text = extract_text_from_file(file)
        
        # Run rule-based checks first
        basic_errors = rule_based_checks(text)
        if basic_errors:
            result = ValidationResult(
                errors=[ValidationError(**e) for e in basic_errors],
                criticality_score=100,
                validation_summary="Failed basic rule-based validation checks",
                clause_matches=[]
            )
            
            # Log validation result
            await ValidationOperations.log_validation(db, {
                "document_id": 0,  # Placeholder, no document created yet
                "status": "failed",
                "message": "Document failed rule-based validation"
            })
            
            return result
        
        # Run LLM-based validation
        llm = LLMValidator()
        llm_result = await llm.validate(text)
        
        # Create final result
        result = ValidationResult(
            errors=llm_result["errors"],
            criticality_score=llm_result["criticality_score"],
            validation_summary=llm_result["validation_summary"],
            clause_matches=[]  # We're not doing clause matching in this example
        )
        
        # Log validation result
        status = "passed" if not llm_result["errors"] else "failed"
        await ValidationOperations.log_validation(db, {
            "document_id": 0,  # Placeholder
            "status": status,
            "message": llm_result["validation_summary"]
        })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")