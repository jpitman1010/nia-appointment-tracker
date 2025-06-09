# crud/encounter.py

import os
from datetime import datetime
from sqlalchemy.orm import Session
from models.models import Encounter, Patient
from typing import Optional, List, Dict

# Placeholder import for PDF generation (you can replace with your preferred library)
# from utils.pdf_generator import generate_pdf_from_text

def create_encounter(
    db: Session,
    patient_id: int,
    provider_id: int,
    encounter_type: str,
    note_text: str,
    structured_note: Optional[Dict] = None,
    created_by: Optional[str] = None,
) -> Encounter:
    """
    Create a new encounter record with raw note text and optional structured JSON note.

    Args:
        db: DB session
        patient_id: ID of the patient
        provider_id: ID of the provider
        encounter_type: Type/category of encounter
        note_text: Full raw clinical note text
        structured_note: JSON/dict representing parsed note sections and flags
        created_by: User who created the encounter

    Returns:
        Encounter object
    """
    encounter = Encounter(
        patient_id=patient_id,
        provider_id=provider_id,
        encounter_type=encounter_type,
        note_text=note_text,
        structured_note=structured_note or {},
        created_by=created_by,
        created_date=datetime.utcnow(),
        deleted=False
    )

    db.add(encounter)
    db.commit()
    db.refresh(encounter)

    # Generate PDF (placeholder)
    # pdf_path = generate_pdf_from_text(note_text, encounter.id)
    # encounter.pdf_path = pdf_path
    # db.commit()

    return encounter


def update_encounter(
    db: Session,
    encounter_id: int,
    note_text: Optional[str] = None,
    structured_note: Optional[Dict] = None,
    updated_by: Optional[str] = None,
) -> Optional[Encounter]:
    """
    Update existing encounter note and structured note data.

    Args:
        db: DB session
        encounter_id: ID of encounter to update
        note_text: New full note text (optional)
        structured_note: New structured note JSON/dict (optional)
        updated_by: User who updated the encounter

    Returns:
        Updated Encounter object or None if not found
    """
    encounter = db.query(Encounter).filter(Encounter.id == encounter_id, Encounter.deleted == False).first()
    if not encounter:
        return None

    if note_text is not None:
        encounter.note_text = note_text

    if structured_note is not None:
        encounter.structured_note = structured_note

    if updated_by:
        encounter.updated_by = updated_by
    encounter.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(encounter)

    # Optionally regenerate PDF on update
    # pdf_path = generate_pdf_from_text(encounter.note_text, encounter.id)
    # encounter.pdf_path = pdf_path
    # db.commit()

    return encounter


def soft_delete_encounter(
    db: Session,
    encounter_id: int,
    deleted_by: Optional[str] = None
) -> Optional[Encounter]:
    """
    Soft delete an encounter by marking deleted flag and setting deleted info.

    Args:
        db: DB session
        encounter_id: ID of encounter to delete
        deleted_by: User who deleted the record

    Returns:
        Encounter object or None if not found
    """
    encounter = db.query(Encounter).filter(Encounter.id == encounter_id, Encounter.deleted == False).first()
    if not encounter:
        return None

    encounter.deleted = True
    encounter.deleted_at = datetime.utcnow()
    encounter.deleted_by = deleted_by

    db.commit()
    db.refresh(encounter)
    return encounter


def get_encounter_by_id(db: Session, encounter_id: int) -> Optional[Encounter]:
    """
    Retrieve a non-deleted encounter by ID.
    """
    return db.query(Encounter).filter(Encounter.id == encounter_id, Encounter.deleted == False).first()


def search_encounters(
    db: Session,
    patient_id: Optional[int] = None,
    provider_id: Optional[int] = None,
    encounter_type: Optional[str] = None,
    search_text: Optional[str] = None,
) -> List[Encounter]:
    """
    Search encounters with optional filters on patient, provider, encounter type,
    and optional full-text search on note_text.

    Returns non-deleted encounters only.
    """
    query = db.query(Encounter).filter(Encounter.deleted == False)

    if patient_id:
        query = query.filter(Encounter.patient_id == patient_id)
    if provider_id:
        query = query.filter(Encounter.provider_id == provider_id)
    if encounter_type:
        query = query.filter(Encounter.encounter_type == encounter_type)
    if search_text:
        # Simple LIKE search - can be replaced with full-text indexing
        like_pattern = f"%{search_text}%"
        query = query.filter(Encounter.note_text.ilike(like_pattern))

    return query.order_by(Encounter.created_date.desc()).all()
