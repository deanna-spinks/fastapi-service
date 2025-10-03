from fastapi import HTTPException

from models.patients import PatientCreate, PatientRead, PatientUpdate
from storage.memory import (
    create_patient,
    delete_patient,
    get_patient,
    list_patients,
    update_patient,
)


async def create_patient_handler(patient: PatientCreate) -> PatientRead:
    return await create_patient(patient)


async def get_patient_handler(patient_id: int) -> PatientRead:
    patient = await get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


async def list_patients_handler() -> list[PatientRead]:
    return await list_patients()


async def update_patient_handler(
    patient_id: int, patient_update: PatientUpdate
) -> PatientRead:
    try:
        return await update_patient(patient_id, patient_update)
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail="Patient not found")
        raise


async def delete_patient_handler(patient_id: int) -> dict:
    try:
        await delete_patient(patient_id)
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail="Patient not found")
        raise
    return {"message": "Patient deleted successfully"}
