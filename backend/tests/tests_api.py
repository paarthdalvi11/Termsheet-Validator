from fastapi.testclient import TestClient
from app.main import app
import os
import pytest
from fastapi.testclient import TestClient

client = TestClient(app)

def test_upload_document():
    response = client.post(
        "/upload_document",
        json={"doc_name": "Test Doc", "uploaded_by": "test@barclays.com"}
    )
    assert response.status_code == 200
    assert "message" in response.json()
    
def test_simple_validation_endpoint(client, sample_termsheet_file):
    """Test the simple validation endpoint with a valid file"""
    with open(sample_termsheet_file, "rb") as f:
        response = client.post(
            "/validate/simple",
            files={"file": ("sample.pdf", f, "application/pdf")}
        )
    
    assert response.status_code == 200
    result = response.json()
    assert "is_valid" in result
    assert isinstance(result["is_valid"], bool)
    assert "message" in result

def test_full_validation_endpoint(client, sample_termsheet_file):
    """Test the full validation endpoint with a valid file"""
    with open(sample_termsheet_file, "rb") as f:
        response = client.post(
            "/validate/full",
            files={"file": ("sample.pdf", f, "application/pdf")}
        )
    
    assert response.status_code == 200
    result = response.json()
    assert "errors" in result
    assert "criticality_score" in result
    assert "validation_summary" in result
    assert "clause_matches" in result
    assert isinstance(result["criticality_score"], int)
    assert 0 <= result["criticality_score"] <= 100

def test_validation_with_invalid_file(client):
    """Test validation with an invalid file type"""
    with open("tests/data/invalid.txt", "wb") as f:
        f.write(b"This is not a valid termsheet")
    
    with open("tests/data/invalid.txt", "rb") as f:
        response = client.post(
            "/validate/full",
            files={"file": ("invalid.txt", f, "text/plain")}
        )
    
    # Should either return 400 for invalid file or 200 with validation errors
    if response.status_code == 400:
        assert "detail" in response.json()
    else:
        assert response.status_code == 200
        result = response.json()
        assert result["criticality_score"] > 50  # High criticality for invalid file

def test_critical_clause_detection_in_api(client, sample_termsheet_file):
    """Test critical clause detection in the API endpoint"""
    with open(sample_termsheet_file, "rb") as f:
        response = client.post(
            "/validate/full",
            files={"file": ("sample_termsheet.pdf", f, "application/pdf")}
        )
    
    assert response.status_code == 200
    result = response.json()
    
    # Check if validation summary mentions critical clauses
    assert "critical clauses" in result["validation_summary"].lower()
    
    # Check if any errors are of type CRITICAL_CLAUSE
    critical_errors = [e for e in result["errors"] if e["type"] == "CRITICAL_CLAUSE"]
    assert len(critical_errors) > 0