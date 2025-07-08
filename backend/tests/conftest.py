import pytest
from fastapi.testclient import TestClient
import os
from app.main import app

@pytest.fixture
def client():
    """Return a TestClient instance for API testing"""
    return TestClient(app)

@pytest.fixture
def sample_termsheet_file():
    """Return path to a sample termsheet file for testing"""
    file_path = os.path.join(os.path.dirname(__file__), "data", "sample_termsheet.pdf")
    return file_path
