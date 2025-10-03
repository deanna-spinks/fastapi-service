from fastapi import APIRouter

from api.handlers.patients import (
    create_patient_handler,
    delete_patient_handler,
    get_patient_handler,
    list_patients_handler,
    update_patient_handler,
)
from models.patients import PatientCreate, PatientRead, PatientUpdate

patients_router = APIRouter(prefix="/patients", tags=["patients"])


@patients_router.get("/")
async def list_patients():
    return await list_patients_handler()


@patients_router.post("/")
async def create_patient(patient: PatientCreate):
    return await create_patient_handler(patient)


@patients_router.get("/{patient_id}")
async def get_patient(patient_id: int):
    return await get_patient_handler(patient_id)


@patients_router.patch("/{patient_id}", response_model=PatientRead)
async def patch_patient(patient_id: int, patient_update: PatientUpdate):
    return await update_patient_handler(patient_id, patient_update)


@patients_router.put("/{patient_id}")
async def update_patient(patient_id: int, patient: PatientUpdate):
    return await update_patient_handler(patient_id, patient)


@patients_router.delete("/{patient_id}")
async def delete_patient(patient_id: int):
    return await delete_patient_handler(patient_id)
