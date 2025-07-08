import json
import numpy as np
import faiss
import os
from app.utils.validation_helpers import get_embedding

# Critical financial clause keywords
CRITICAL_KEYWORDS = [
    "Change of Control", "Put Option", "Redemption", "Issuer Call", "Make-Whole",
    "Early Redemption", "Default", "Interest Payment", "Coupon", "Rate(s) of Interest",
    "Floating Rate", "Zero Coupon", "Fixed Rate", "Interest Commencement", "Maturity Date"
]

def is_critical_clause(text):
    """Check if text contains critical financial terms"""
    for keyword in CRITICAL_KEYWORDS:
        if keyword.lower() in text.lower():
            return True
    return False

def detect_critical_clauses(chunks, top_k=5):
    """
    Detect critical clauses in chunked text
    
    Args:
        chunks: List of text chunks from the termsheet
        top_k: Number of top matches to consider
        
    Returns:
        Dictionary with is_critical flag and list of critical chunks
    """
    # Create vectors for chunks
    vectors = []
    for chunk in chunks:
        vector = get_embedding(chunk)
        vectors.append(vector)
    
    # Build FAISS index
    vectors_array = np.array(vectors).astype('float32')
    dim = vectors_array.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors_array)
    
    # Query for financial terms
    query_text = "financial terms and conditions"
    query_vector = get_embedding(query_text)
    query_vector = np.array(query_vector).astype('float32').reshape(1, -1)
    
    # Search for similar chunks
    distances, indices = index.search(query_vector, top_k)
    
    # Check if any top chunks are critical
    critical_chunks = []
    for i, idx in enumerate(indices[0]):
        if idx < len(chunks):
            content = chunks[idx]
            if is_critical_clause(content):
                critical_chunks.append({
                    "chunk_id": idx,
                    "text": content.strip()
                })
    
    return {
        "is_critical": len(critical_chunks) > 0,
        "critical_chunks": critical_chunks
    }

def build_validation_prompt(critical_clauses):
    """Build prompt for LLM validation"""
    prompt = """
    The following are critical clauses from a financial termsheet. 
    Validate if the termsheet is valid or not valid.
    
    Provide your response in a SINGLE, COHERENT analysis with this structure:
    1. Validation: valid or not valid
    2. Justification: explain why the termsheet is valid or not valid
    3. One final summary section
    
    Clauses to validate:
    """
    
    for i, clause in enumerate(critical_clauses, 1):
        prompt += f"\n{i}. {clause['text']}\n"
        
    return prompt
