import pytest
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def sample_activity():
    """Return a sample activity for testing"""
    return {
        "description": "Test Activity",
        "schedule": "Monday 3:00 PM",
        "max_participants": 10,
        "participants": []
    }
