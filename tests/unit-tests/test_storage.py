from unittest.mock import patch

import pytest

from src.models.patients import PatientCreate, PatientUpdate
from src.storage.memory import (
    create_patient,
    delete_patient,
    get_patient,
    list_patients,
    patients,
    update_patient,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestPatientStorage:
    """Test patient storage functions"""

    async def _create_test_patient(
        self, patient_data_factory, patient_id: int = 1, **overrides
    ):
        """Helper to create a patient with optional field overrides"""
        data = patient_data_factory(**overrides)
        with patch("src.storage.memory.get_next_id", return_value=patient_id):
            return await create_patient(PatientCreate(**data))

    async def test_create_patient(self, patient_data_factory):
        """Test creating a patient"""
        with patch("src.storage.memory.get_next_id", return_value=1):
            data = patient_data_factory(name="John Doe", email="john@example.com")
            patient_data = PatientCreate(**data)

            result = await create_patient(patient_data)

            assert result.patient_id == 1
            assert result.name == "John Doe"
            assert 1 in patients

    async def test_get_patient_exists(self, patient_data_factory):
        """Test getting a patient that exists"""
        await self._create_test_patient(patient_data_factory, 1, name="Jane Doe")

        result = await get_patient(1)

        assert result is not None
        assert result.patient_id == 1
        assert result.name == "Jane Doe"

    async def test_get_patient_not_found(self):
        """Test getting a patient that doesn't exist"""
        result = await get_patient(999)
        assert result is None

    async def test_list_patients_empty(self):
        """Test listing patients when storage is empty"""
        result = await list_patients()
        assert result == []

    async def test_list_patients_multiple(self):
        """Test listing multiple patients"""
        # Create multiple patients
        with patch("src.storage.memory.get_next_id", side_effect=[1, 2, 3]):
            await create_patient(
                PatientCreate(
                    name="Patient 1",
                    age=30,
                    gender="male",
                    email="patient1@example.com",
                    phone="1111111111",
                )
            )
            await create_patient(
                PatientCreate(
                    name="Patient 2",
                    age=40,
                    gender="female",
                    email="patient2@example.com",
                    phone="2222222222",
                )
            )
            await create_patient(
                PatientCreate(
                    name="Patient 3",
                    age=50,
                    gender="other",
                    email="patient3@example.com",
                    phone="3333333333",
                )
            )

        result = await list_patients()

        assert len(result) == 3
        assert result[0].patient_id == 1
        assert result[1].patient_id == 2
        assert result[2].patient_id == 3

    async def test_update_patient_success(self):
        """Test partial update preserves unchanged fields"""
        await self._create_test_patient(
            1, name="Original", email="original@example.com"
        )

        result = await update_patient(1, PatientUpdate(name="Updated"))

        assert result.patient_id == 1
        assert result.name == "Updated"
        assert result.email == "original@example.com"  # Unchanged

    async def test_update_patient_not_found(self):
        """Test updating a patient that doesn't exist"""
        update_data = PatientUpdate(name="Test")

        with pytest.raises(ValueError, match="Patient with id 999 not found"):
            await update_patient(999, update_data)

    async def test_delete_patient_success(self):
        """Test deleting a patient successfully"""
        await self._create_test_patient(1)

        await delete_patient(1)

        assert 1 not in patients

    async def test_delete_patient_not_found(self):
        """Test deleting a patient that doesn't exist"""
        with pytest.raises(ValueError, match="Patient with id 999 not found"):
            await delete_patient(999)
