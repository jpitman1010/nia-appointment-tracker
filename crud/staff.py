# staff.py

from sqlalchemy.orm import Session
from models import Staff
from schemas import StaffCreate, StaffUpdate
from crud.generic import search_entities


def create_staff(db: Session, staff: StaffCreate):
    db_staff = Staff(**staff.dict())
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff


def update_staff(db: Session, staff_id: int, staff_update: StaffUpdate):
    db_staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not db_staff:
        return None
    for field, value in staff_update.dict(exclude_unset=True).items():
        setattr(db_staff, field, value)
    db.commit()
    db.refresh(db_staff)
    return db_staff


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
