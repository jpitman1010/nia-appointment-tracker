# staff.py

from schemas import StaffCreate, StaffUpdate
from crud.generic import search_entities
from models.models import Staff, db
from sqlalchemy.orm import Session
from models import Staff
from crud.generic import search_entities  # Your fuzzy search utility

def search_staff(db: Session, query: str):
    # Search staff by fname, lname, email with fuzzy logic
    return search_entities(db.query(Staff), Staff, query, fields=["fname", "lname", "email"])

def create_staff(db: Session, staff_data: dict):
    """
    Create and return a new staff member.
    staff_data should be a dict with keys: email, password, fname, lname, role, enabled
    """
    staff = Staff(**staff_data)
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff

def update_staff(db: Session, staff_id: int, updates: dict):
    """
    Update staff info by id.
    updates is a dict of field:value pairs to update.
    """
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        return None
    for key, value in updates.items():
        if hasattr(staff, key):
            setattr(staff, key, value)
    db.commit()
    db.refresh(staff)
    return staff


def delete_staff(db: Session, staff_id: int):
    db_staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if db_staff:
        db.delete(db_staff)
        db.commit()
    return db_staff


def get_staff_by_id(db: Session, staff_id: int):
    return db.query(Staff).filter(Staff.id == staff_id).first()


def get_all_staff(db: Session):
    return db.query(Staff).all()


def search_staff(db: Session, query: str):
    return search_entities(db.query(Staff), Staff, query, fields=["fname", "lname", "email", "department"])


def get_staff_by_email(db: Session, email: str):
    return db.query(Staff).filter_by(email=email).first()

def get_staff_id(db: Session, email: str):
    result = db.query(Staff.id).filter_by(email=email).first()
    return result[0] if result else None


def get_staff_fname(db: Session, email: str):
    result = db.query(Staff.fname).filter_by(email=email).first()
    return result[0] if result else None


def get_staff_name(db: Session, email: str):
    result = db.query(Staff.fname, Staff.lname).filter_by(email=email).first()
    if result:
        return f"{result[0]} {result[1]}"
    return None


def check_if_valid_user(db: Session, email: str):
    return db.query(Staff).filter_by(email=email).first() is not None


def password_check(db: Session, email: str, password: str):
    staff = db.query(Staff).filter_by(email=email, password=password).first()
    return staff is not None
