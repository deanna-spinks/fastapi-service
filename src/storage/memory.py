from typing import Dict

from src.models.patients import PatientCreate, PatientRead, PatientUpdate
from src.utils.id_generator import get_next_id

patients: Dict[int, PatientRead] = {}


async def create_patient(patient: PatientCreate) -> PatientRead:
    patient_id = get_next_id()
    patient_obj = PatientRead(patient_id=patient_id, **patient.model_dump())
    patients[patient_id] = patient_obj
    return patient_obj


async def get_patient(patient_id: int) -> PatientRead | None:
    return patients.get(patient_id)


async def list_patients() -> list[PatientRead]:
    return list(patients.values())


async def update_patient(patient_id: int, patient: PatientUpdate) -> PatientRead:
    existing_patient = patients.get(patient_id)
    if not existing_patient:
        raise ValueError(f"Patient with id {patient_id} not found")

    # Merge existing data with updates
    update_data = patient.model_dump(exclude_unset=True)
    updated_data = existing_patient.model_dump()
    updated_data.update(update_data)

    patients[patient_id] = PatientRead(**updated_data)
    return patients[patient_id]


async def delete_patient(patient_id: int) -> None:
    if patient_id not in patients:
        raise ValueError(f"Patient with id {patient_id} not found")
    del patients[patient_id]
