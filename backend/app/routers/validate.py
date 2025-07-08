import logging
import traceback
from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import os
import hashlib
import json
import ollama
import numpy as np
from app.utils.critical_clause_detector import detect_critical_clauses, build_validation_prompt
from app.dependencies import get_db
from app.schemas import SimpleValidationResult, ValidationResult, ValidationError, ClauseMatch, Severity

# Initialize logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/validate", tags=["Validation"])

# ---------- Document Reading Functions ----------
def read_pdf(file: UploadFile) -> str:
    from PyPDF2 import PdfReader
    content = ""
    reader = PdfReader(file.file)
    for page in reader.pages:
        content += page.extract_text() or ""
    return content

def read_docx(file: UploadFile) -> str:
    import docx
    doc = docx.Document(file.file)
    return "\n".join([para.text for para in doc.paragraphs])

def read_txt(file: UploadFile) -> str:
    return file.file.read().decode("utf-8")

def extract_text_from_file(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[1].lower()
    file.file.seek(0)

    if ext == ".pdf":
        return read_pdf(file)
    elif ext == ".docx":
        return read_docx(file)
    elif ext == ".txt":
        return read_txt(file)
    else:
        raise ValueError("Unsupported file type")

# ---------- Basic Validation ----------
def validate_termsheet_content(text: str) -> list:
    required_sections = ["Interest", "Collateral", "Maturity", "Issuer"]
    missing = [section for section in required_sections if section.lower() not in text.lower()]
    return missing

# ---------- Embedding Utilities ----------
def get_embedding(text: str) -> np.ndarray:
    result = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return np.array(result['embedding'], dtype=np.float32)

def chunk_text(text: str, max_length: int = 300) -> list:
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    return paragraphs

# ---------- LLM Validator ----------
class TermsheetValidator:
    def __init__(self):
        self.validation_prompt = """
        Analyze this term sheet as a senior banking compliance officer:
        {text}

        Validate these aspects:
        1. Interest rate calculations (verify math)
        2. Date formats (must be YYYY-MM-DD)
        3. Missing collateral clauses
        4. Compliance with SEC Rule 10b-5 and MiFID II
        5. Cross-referencing with base prospectus

        Respond with this exact JSON structure:
        {{
            "errors": [
                {{
                    "type": "ERROR_TYPE",
                    "description": "Specific issue found",
                    "section": "Document section",
                    "severity": "CRITICAL/HIGH/MEDIUM/LOW"
                }}
            ],
            "criticality_score": 0-100,
            "validation_summary": "Brief risk assessment"
        }}
        """

    async def validate_with_ollama(self, text: str) -> dict:
        try:
            response = ollama.generate(
                model="mistral",
                prompt=self.validation_prompt.format(text=text),
                format="json",
                options={"temperature": 0.0, "num_ctx": 16000}
            )
            # Extract JSON from response
            result = json.loads(response["response"])
            return result
        except Exception as e:
            logger.error(f"LLM validation failed: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"LLM validation failed: {str(e)}")

# ---------- FAISS Clause Matcher ----------
class FaissClauseMatcher:
    def __init__(self, reference_clauses: list):
        import faiss
        self.ref_clauses = reference_clauses
        self.index = faiss.IndexFlatL2(768)  # Dimension of nomic-embed-text
        self.clause_text_map = {}
        self._build_index()

    def _build_index(self):
        embeddings = []
        for clause in self.ref_clauses:
            emb = get_embedding(clause)
            hash_id = hashlib.md5(clause.encode()).hexdigest()
            self.clause_text_map[hash_id] = clause
            embeddings.append(emb)
        embeddings = np.vstack(embeddings)
        self.index.add(embeddings)

    def match(self, uploaded_clauses: list) -> list:
        matches = []
        for clause in uploaded_clauses:
            emb = get_embedding(clause).reshape(1, -1)
            D, I = self.index.search(emb, 1)
            similarity = 1 / (1 + D[0][0])
            match_type = "match" if similarity > 0.9 else "partial" if similarity > 0.75 else "missing"
            matches.append(ClauseMatch(
                clause=clause, 
                match_type=match_type, 
                similarity=float(similarity)
            ))
        return matches

# ---------- Endpoints ----------
@router.post("/simple", response_model=SimpleValidationResult)
async def simple_validate_termsheet(file: UploadFile = File(...)):
    """
    Simple binary validation of termsheet format
    """
    try:
        contents = await file.read()
        if b"Termsheet" in contents or b"Interest" in contents:
            return SimpleValidationResult(is_valid=True, message="Valid termsheet format.")
        else:
            return SimpleValidationResult(is_valid=False, message="Invalid file or missing 'Termsheet' content.")
    except Exception as e:
        logger.error(f"Simple validation failed: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@router.post("/full", response_model=ValidationResult)
async def full_validate_termsheet(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Comprehensive validation of termsheet with detailed analysis
    """
    try:
        text = extract_text_from_file(file)
    except Exception as e:
        logger.error(f"File parsing failed: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=f"File parsing failed: {str(e)}")

    # Step 0: Basic keyword check
    missing_keywords = validate_termsheet_content(text)
    if missing_keywords:
        return ValidationResult(
            errors=[ValidationError(
                type="STRUCTURE",
                description=f"Missing required sections: {', '.join(missing_keywords)}",
                section="Header",
                severity=Severity.CRITICAL
            )],
            criticality_score=100,
            validation_summary="Invalid document structure",
            clause_matches=[]
        )

    # Step 1: LLM Validation
    validator = TermsheetValidator()
    llm_result = await validator.validate_with_ollama(text)

    # Step 2: Clause-Level Matching
    uploaded_clauses = chunk_text(text)
    reference_clauses = [
        "The interest rate shall be 5.5% per annum.",
        "The issuer shall provide collateral in the form of government bonds.",
        "The maturity date shall not exceed 2029-12-31."
    ]
    
    matcher = FaissClauseMatcher(reference_clauses)
    clause_matches = matcher.match(uploaded_clauses)

    # Log successful validation
    logger.info(f"Successfully validated termsheet with criticality score: {llm_result['criticality_score']}")

    # Create and return final result
    return ValidationResult(
        errors=llm_result["errors"],
        criticality_score=llm_result["criticality_score"],
        validation_summary=llm_result["validation_summary"],
        clause_matches=clause_matches
    )

# In app/routers/validate.py
@router.post("/critical", response_model=Dict[str, Any])
async def detect_critical_clauses_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Detect critical financial clauses in a termsheet
    """
    try:
        text = extract_text_from_file(file)
        chunks = chunk_text(text)
        result = detect_critical_clauses(chunks)
        return result
    except Exception as e:
        logger.error(f"Critical clause detection failed: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")
