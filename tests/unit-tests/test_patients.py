import pytest


@pytest.mark.unit
def test_list_patients_empty(client):
    """Test listing patients API returns proper response structure"""
    response = client.get("/patients/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Should return a list
    # Note: We don't check for empty list since other tests may have run first


@pytest.mark.unit
def test_create_patient(client, sample_patient_data):
    """Test creating a new patient"""
    response = client.post("/patients/", json=sample_patient_data)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == sample_patient_data["name"]
    assert data["age"] == sample_patient_data["age"]
    assert data["gender"] == sample_patient_data["gender"]
    assert data["email"] == sample_patient_data["email"]
    assert data["phone"] == sample_patient_data["phone"]
    assert "patient_id" in data
    assert isinstance(data["patient_id"], int)


@pytest.mark.unit
def test_get_patient(client, create_patient):
    """Test getting a specific patient"""
    # Create a patient using factory fixture
    created_patient = create_patient()
    patient_id = created_patient["patient_id"]

    # Now get the patient
    response = client.get(f"/patients/{patient_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["patient_id"] == patient_id
    assert data["name"] == created_patient["name"]
    assert data["age"] == created_patient["age"]
    assert data["gender"] == created_patient["gender"]
    assert data["email"] == created_patient["email"]
    assert data["phone"] == created_patient["phone"]


@pytest.mark.unit
def test_list_patients_after_creation(client):
    """Test listing patients after creating some"""
    # Create multiple patients
    patients = [
        {
            "name": "Alice Johnson",
            "age": 35,
            "gender": "female",
            "email": "alice@example.com",
            "phone": "1111111111",
        },
        {
            "name": "Bob Wilson",
            "age": 40,
            "gender": "male",
            "email": "bob@example.com",
            "phone": "2222222222",
        },
    ]

    created_ids = []
    for patient in patients:
        response = client.post("/patients/", json=patient)
        assert response.status_code == 200
        created_ids.append(response.json()["patient_id"])

    # List all patients
    response = client.get("/patients/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) >= 2  # At least the two we created

    # Check that our created patients are in the list
    patient_ids = [p["patient_id"] for p in data]
    for pid in created_ids:
        assert pid in patient_ids


@pytest.mark.unit
def test_update_patient_partial(client, create_patient):
    """Test partially updating a patient with PATCH"""
    # Create a patient using factory fixture
    created_patient = create_patient()
    patient_id = created_patient["patient_id"]

    # Update only some fields
    update_data = {"age": 35, "phone": "6666666666"}

    response = client.patch(f"/patients/{patient_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["patient_id"] == patient_id
    assert data["name"] == created_patient["name"]  # Should remain unchanged
    assert data["age"] == 35  # Should be updated
    assert data["gender"] == created_patient["gender"]  # Should remain unchanged
    assert data["email"] == created_patient["email"]  # Should remain unchanged
    assert data["phone"] == "6666666666"  # Should be updated


@pytest.mark.unit
def test_delete_patient(client, create_patient):
    """Test deleting a patient"""
    # Create a patient using factory fixture
    created_patient = create_patient()
    patient_id = created_patient["patient_id"]

    # Delete the patient
    response = client.delete(f"/patients/{patient_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Patient deleted successfully"}

    # Try to get the patient - should fail
    response = client.get(f"/patients/{patient_id}")
    assert response.status_code == 404


@pytest.mark.unit
def test_get_patient_not_found(client):
    """Test getting a patient that doesn't exist"""
    response = client.get("/patients/99999")
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.unit
def test_patch_patient_not_found(client):
    """Test patching a patient that doesn't exist"""
    update_data = {"name": "Non-existent"}
    response = client.patch("/patients/99999", json=update_data)
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.unit
def test_delete_patient_not_found(client):
    """Test deleting a patient that doesn't exist"""
    response = client.delete("/patients/99999")
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.unit
def test_create_patient_invalid_data(client):
    """Test creating a patient with invalid data"""
    # Missing required fields
    invalid_data = {"name": "Invalid Patient"}
    response = client.post("/patients/", json=invalid_data)
    assert response.status_code == 422  # Validation error

    # Invalid email
    invalid_data = {
        "name": "Invalid Patient",
        "age": 30,
        "gender": "male",
        "email": "invalid-email",
        "phone": "1234567890",
    }
    response = client.post("/patients/", json=invalid_data)
    assert response.status_code == 422  # Validation error


@pytest.mark.unit
def test_create_patient_duplicate_email(client):
    """Test creating patients with duplicate emails (if we add uniqueness constraint)"""
    # For now, this should work since we don't enforce uniqueness
    patient1 = {
        "name": "Patient 1",
        "age": 30,
        "gender": "male",
        "email": "duplicate@example.com",
        "phone": "1234567890",
    }
    patient2 = {
        "name": "Patient 2",
        "age": 25,
        "gender": "female",
        "email": "duplicate@example.com",
        "phone": "0987654321",
    }

    response1 = client.post("/patients/", json=patient1)
    assert response1.status_code == 200

    response2 = client.post("/patients/", json=patient2)
    assert response2.status_code == 200  # Currently allowed


@pytest.mark.unit
def test_update_patient_partial_empty_patch(client, create_patient):
    """Test patching with no data provided"""
    # Create a patient using factory fixture
    created_patient = create_patient()
    patient_id = created_patient["patient_id"]

    # Patch with empty data
    response = client.patch(f"/patients/{patient_id}", json={})
    assert response.status_code == 200

    # Data should remain unchanged
    data = response.json()
    assert data["name"] == created_patient["name"]
    assert data["age"] == created_patient["age"]
