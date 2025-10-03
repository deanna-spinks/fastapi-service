from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    email: EmailStr
    phone: str


class PatientRead(PatientCreate):
    patient_id: int


# Used for partial updates with PATCH /patients/{id}.
# All fields are optional, because in a PATCH request, the client may update only one
# field.
# Default is None, so you can check which fields were actually provided
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


# Represents internal storage, including sensitive fields like password hashes or
# timestamps, not returned to the client. Never use this model in your response schemas,
# only internally in handlers or CRUD functions
class PatientInDB(PatientRead):
    created_at: datetime
    updated_at: datetime
