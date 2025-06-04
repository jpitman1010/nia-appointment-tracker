# clinician.py

from models.models import Clinician, db
from sqlalchemy.orm import Session
from schemas import ClinicianCreate, ClinicianUpdate
from crud.generic import search_entities

def create_clinician(db: Session, clinician: ClinicianCreate):
    db_clinician = Clinician(**clinician.dict())
    db.add(db_clinician)
    db.commit()
    db.refresh(db_clinician)
    return db_clinician

def update_clinician(db: Session, clinician_id: int, clinician_update: ClinicianUpdate):
    clinician = db.query(Clinician).filter(Clinician.id == clinician_id).first()
    if not clinician:
        return None
    for field, value in clinician_update.dict(exclude_unset=True).items():
        setattr(clinician, field, value)
    db.commit()
    db.refresh(clinician)
    return clinician

def delete_clinician(db: Session, clinician_id: int):
    clinician = db.query(Clinician).filter(Clinician.id == clinician_id).first()
    if clinician:
        db.delete(clinician)
        db.commit()
    return clinician

def get_clinician_by_id(db: Session, clinician_id: int):
    return db.query(Clinician).filter(Clinician.id == clinician_id).first()

def get_all_clinicians(db: Session):
    return db.query(Clinician).all()

def search_clinicians(db: Session, query: str):
    return search_entities(db.query(Clinician), Clinician, query, fields=["fname", "lname", "email", "specialty"])
