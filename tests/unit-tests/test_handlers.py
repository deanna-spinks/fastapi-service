from unittest.mock import patch

import pytest
from fastapi import HTTPException

from src.api.exceptions import handle_not_found_error
from src.api.handlers.patients import (  # noqa: F401
    delete_patient_handler,
    update_patient_handler,
)
from src.models.patients import PatientUpdate


@pytest.mark.unit
class TestHandleNotFoundError:
    """Test the shared handle_not_found_error helper function"""

    @pytest.mark.parametrize(
        "error_message,should_convert",
        [
            # Should convert to 404
            ("Patient with id 1 not found", True),
            ("PATIENT WITH ID 1 NOT FOUND", True),
            ("Not Found", True),
            ("patient NOT FOUND", True),
            # Should re-raise original error
            ("Database connection failed", False),
            ("Invalid input", False),
        ],
    )
    def test_handle_not_found_error(self, error_message, should_convert):
        """Test that handle_not_found_error correctly converts or re-raises errors"""
        error = ValueError(error_message)

        if should_convert:
            with pytest.raises(HTTPException) as exc_info:
                handle_not_found_error(error)
            assert exc_info.value.status_code == 404
            assert exc_info.value.detail == error_message
        else:
            with pytest.raises(ValueError, match=error_message):
                handle_not_found_error(error)


@pytest.mark.unit
@pytest.mark.asyncio
class TestPatientHandlers:
    """Test patient handler functions"""

    @pytest.mark.parametrize(
        "handler_func,storage_func,handler_args,error_type,should_convert",
        [
            # Update handler - should reraise non-not-found errors
            (
                "update_patient_handler",
                "update_patient",
                {"patient_id": 1, "patient_update": PatientUpdate(name="Test")},
                "Database connection failed",
                False,
            ),
            # Delete handler - should reraise non-not-found errors
            (
                "delete_patient_handler",
                "delete_patient",
                {"patient_id": 1},
                "Database connection failed",
                False,
            ),
            # Update handler - should convert not-found errors
            (
                "update_patient_handler",
                "update_patient",
                {"patient_id": 1, "patient_update": PatientUpdate(name="Test")},
                "Patient with id 1 not found",
                True,
            ),
            # Delete handler - should convert not-found errors
            (
                "delete_patient_handler",
                "delete_patient",
                {"patient_id": 1},
                "Patient with id 1 not found",
                True,
            ),
        ],
    )
    async def test_handler_error_handling(
        self, handler_func, storage_func, handler_args, error_type, should_convert
    ):
        """Test that handlers correctly handle errors via handle_not_found_error"""
        with patch(f"src.api.handlers.patients.{storage_func}") as mock_storage:
            mock_storage.side_effect = ValueError(error_type)

            if should_convert:
                # Should convert to HTTPException 404
                with pytest.raises(HTTPException) as exc_info:
                    await eval(f"{handler_func}")(**handler_args)
                assert exc_info.value.status_code == 404
                assert exc_info.value.detail == error_type
            else:
                # Should re-raise original ValueError
                with pytest.raises(ValueError, match=error_type):
                    await eval(f"{handler_func}")(**handler_args)

    @pytest.mark.parametrize(
        "handler_func,storage_func,handler_args,expected_result",
        [
            # Update handler success
            (
                "update_patient_handler",
                "update_patient",
                {
                    "patient_id": 1,
                    "patient_update": PatientUpdate(name="Updated Patient"),
                },
                {
                    "patient_id": 1,
                    "name": "Updated Patient",
                    "age": 30,
                    "gender": "male",
                    "email": "test@example.com",
                    "phone": "1234567890",
                },
            ),
            # Delete handler success
            (
                "delete_patient_handler",
                "delete_patient",
                {"patient_id": 1},
                {"message": "Patient deleted successfully"},
            ),
        ],
    )
    async def test_handler_success(
        self, handler_func, storage_func, handler_args, expected_result
    ):
        """Test successful handler operations"""
        with patch(f"src.api.handlers.patients.{storage_func}") as mock_storage:
            if handler_func == "update_patient_handler":
                mock_storage.return_value = expected_result

            result = await eval(f"{handler_func}")(**handler_args)

            assert result == expected_result
            if handler_func == "update_patient_handler":
                mock_storage.assert_called_once_with(1, handler_args["patient_update"])
            else:
                mock_storage.assert_called_once_with(1)
