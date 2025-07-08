# tests/test_critical_detector.py
import pytest
from app.utils.critical_clause_detector import detect_critical_clauses, build_validation_prompt
from app.utils.validation_helpers import chunk_text

def test_critical_clause_detection():
    """Test that critical clauses are properly detected"""
    # Sample text with critical clauses
    text = """
    This agreement includes a Change of Control provision.
    The Interest Rate shall be 5.5% per annum.
    Early Redemption is permitted with 30 days notice.
    """
    
    # Chunk the text
    chunks = chunk_text(text)
    
    # Run detection
    result = detect_critical_clauses(chunks)
    
    # Assertions
    assert result["is_critical"] == True
    assert len(result["critical_chunks"]) > 0
    # Check that specific keywords were detected
    detected_keywords = [chunk["text"].lower() for chunk in result["critical_chunks"]]
    assert any("change of control" in keyword for keyword in detected_keywords)
    assert any("early redemption" in keyword for keyword in detected_keywords)

def test_build_validation_prompt():
    """Test that validation prompts are correctly built"""
    critical_clauses = [
        {"chunk_id": 1, "text": "The Interest Rate shall be 5.5% per annum."},
        {"chunk_id": 2, "text": "Early Redemption is permitted with 30 days notice."}
    ]
    
    prompt = build_validation_prompt(critical_clauses)
    
    # Check prompt structure
    assert "The following are critical clauses" in prompt
    assert "Interest Rate" in prompt
    assert "Early Redemption" in prompt
