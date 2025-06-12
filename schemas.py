#Implement full schemas (recommended eventually)
#Use Pydantic or Marshmallow to create comprehensive schemas for each model, including field types and validation. I can help generate these if you want.


# schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Staff schemas
class StaffCreate(BaseModel):
    fname: str
    lname: str
    email: str
    password: str

class StaffUpdate(BaseModel):
    fname: Optional[str] = None
    lname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    enabled: Optional[bool] = None

# Appointment schemas
class AppointmentCreate(BaseModel):
    patient_id: int
    provider_id: int
    scheduled_start: datetime
    scheduled_end: Optional[datetime] = None
    scheduled_by: Optional[str] = None

class AppointmentUpdate(BaseModel):
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    scheduled_by: Optional[str] = None

# Provider (Clinician) schemas
class ProviderCreate(BaseModel):
    fname: str
    lname: str
    type: Optional[str] = None
    email: str

class ProviderUpdate(BaseModel):
    fname: Optional[str] = None
    lname: Optional[str] = None
    type: Optional[str] = None
    email: Optional[str] = None

# Research Study schemas
class ResearchStudyCreate(BaseModel):
    name: str
    principal_investigator: Optional[str] = None
    coordinator: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ResearchStudyUpdate(BaseModel):
    name: Optional[str] = None
    principal_investigator: Optional[str] = None
    coordinator: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ResearchStudyFieldCreate(BaseModel):
    study_id: int
    field_name: str
    field_type: str
    is_required: Optional[bool] = False

class ResearchStudyResponseCreate(BaseModel):
    study_id: int
    patient_id: int
    filled_out_by: Optional[str] = None

# Add more schemas here as needed

