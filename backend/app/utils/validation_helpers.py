import re
import hashlib
import numpy as np
import ollama
import os
from typing import List, Dict, Any, Optional
from fastapi import UploadFile, HTTPException

def sha256_hash(text: str) -> str:
    """Generate SHA-256 hash of input text"""
    return hashlib.sha256(text.encode()).hexdigest()

def rule_based_checks(text: str) -> Optional[List[Dict[str, Any]]]:
    """
    Perform basic rule-based validation checks on document text.
    Returns a list of validation errors or None if checks pass.
    """
    errors = []
    
    # Check for required sections
    required_sections = ["Interest", "Collateral", "Maturity", "Issuer"]
    for section in required_sections:
        if section.lower() not in text.lower():
            errors.append({
                "type": "MISSING_SECTION",
                "description": f"Required section '{section}' is missing",
                "section": "Document Structure",
                "severity": "CRITICAL"
            })
    
    # Check date formats (YYYY-MM-DD)
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    dates = re.findall(date_pattern, text)
    
    # If dates are present but seem invalid
    for date in dates:
        year, month, day = date.split('-')
        if not (1900 <= int(year) <= 2100 and 1 <= int(month) <= 12 and 1 <= int(day) <= 31):
            errors.append({
                "type": "INVALID_DATE",
                "description": f"Invalid date format: {date}",
                "section": "Dates",
                "severity": "HIGH"
            })
    
    # Check for percentage values without % symbol
    percentage_pattern = r'\b\d+(\.\d+)?\s*percent\b'
    percentages = re.findall(percentage_pattern, text.lower())
    if percentages:
        errors.append({
            "type": "FORMAT_ISSUE",
            "description": "Percentages should use % symbol rather than spelled out 'percent'",
            "section": "Interest Rates",
            "severity": "MEDIUM"
        })
    
    return errors if errors else None

def extract_text_from_file(file: UploadFile) -> str:
    """Extract text from PDF, DOCX, or TXT files."""
    ext = os.path.splitext(file.filename)[1].lower()
    file.file.seek(0)

    try:
        if ext == ".pdf":
            return read_pdf(file)
        elif ext == ".docx":
            return read_docx(file)
        elif ext == ".txt":
            return read_txt(file)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File parsing failed: {str(e)}")

def read_pdf(file: UploadFile) -> str:
    """Extract text from PDF file."""
    from PyPDF2 import PdfReader
    content = ""
    reader = PdfReader(file.file)
    for page in reader.pages:
        content += page.extract_text() or ""
    return content

def read_docx(file: UploadFile) -> str:
    """Extract text from DOCX file."""
    import docx
    doc = docx.Document(file.file)
    return "\n".join([para.text for para in doc.paragraphs])

def read_txt(file: UploadFile) -> str:
    """Extract text from TXT file."""
    return file.file.read().decode("utf-8")

def validate_termsheet_content(text: str) -> list:
    """Check if required sections are present in the termsheet."""
    required_sections = ["Interest", "Collateral", "Maturity", "Issuer"]
    missing = [section for section in required_sections if section.lower() not in text.lower()]
    return missing

def get_embedding(text: str) -> np.ndarray:
    """Get embedding vector for text using Ollama."""
    result = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return np.array(result['embedding'], dtype=np.float32)

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks for processing
    """
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = min(start + chunk_size, text_len)
        
        # Avoid cutting words in the middle
        if end < text_len:
            # Find the last space within chunk
            last_space = text.rfind(' ', start, end)
            if last_space != -1:
                end = last_space + 1
        
        chunks.append(text[start:end])
        start = end - overlap if end - overlap > start else end
    
    return chunks
