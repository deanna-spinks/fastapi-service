import os
import sys

import pytest
from faker import Faker
from fastapi.testclient import TestClient

# Add the parent directory to the path so we can import src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.main import app  # noqa: E402
from src.storage.memory import patients  # noqa: E402


@pytest.fixture
def client():
    """FastAPI test client fixture"""
    return TestClient(app)


@pytest.fixture
def faker():
    """Faker instance for generating test data"""
    return Faker()


@pytest.fixture(autouse=True, scope="function")
def clear_patients():
    """Clear in-memory storage before each test function"""
    # Clear before test
    patients.clear()
    yield
    # Clear after test to ensure clean state
    patients.clear()


@pytest.fixture
def sample_patient_data(faker):
    """Generate sample patient data for testing"""
    return {
        "name": faker.name(),
        "age": faker.random_int(min=1, max=120),
        "gender": faker.random_element(["male", "female", "other"]),
        "email": faker.email(),
        "phone": faker.phone_number(),
    }


@pytest.fixture
def create_patient(client, sample_patient_data):
    """Factory fixture to create a patient and return its data"""

    def _create_patient(patient_data=None):
        """Create a patient with optional custom data"""
        data = patient_data or sample_patient_data
        response = client.post("/patients/", json=data)
        assert response.status_code == 200
        return response.json()

    return _create_patient


@pytest.fixture
def static_patient_data():
    """Static patient data for predictable testing"""
    return {
        "name": "Test Patient",
        "age": 30,
        "gender": "male",
        "email": "test@example.com",
        "phone": "1234567890",
    }


@pytest.fixture
def patient_data_factory():
    """Factory to create custom patient data with overrides"""

    def _make_patient_data(**overrides):
        """Create patient data with optional field overrides"""
        defaults = {
            "name": "Test Patient",
            "age": 30,
            "gender": "male",
            "email": "test@example.com",
            "phone": "1234567890",
        }
        return {**defaults, **overrides}

    return _make_patient_data
