# crud/research.py

from sqlalchemy.orm import Session
from models.models import ResearchStudy, ResearchStudyField, ResearchStudyResponse, ResearchStudyFieldResponse
from schemas import ResearchStudyCreate, ResearchStudyUpdate, ResearchStudyFieldCreate, ResearchStudyResponseCreate

def create_research_study(db: Session, study_data: ResearchStudyCreate):
    """Create a new research study with core fixed fields."""
    db_study = ResearchStudy(
        name=study_data.name,
        principal_investigator=study_data.principal_investigator,
        coordinator=study_data.coordinator,
        criteria_entered_by=study_data.criteria_entered_by,
        start_date=study_data.start_date,
        end_date=study_data.end_date,
        created_by=study_data.created_by,
    )
    db.add(db_study)
    db.commit()
    db.refresh(db_study)
    return db_study

def get_research_study(db: Session, study_id: int):
    return db.query(ResearchStudy).filter(ResearchStudy.id == study_id).first()

def update_research_study(db: Session, study_id: int, update_data: ResearchStudyUpdate):
    study = get_research_study(db, study_id)
    if not study:
        return None
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(study, field, value)
    db.commit()
    db.refresh(study)
    return study

def delete_research_study(db: Session, study_id: int, deleted_by: str):
    study = get_research_study(db, study_id)
    if not study:
        return None
    study.deleted = True
    study.deleted_by = deleted_by
    study.deleted_at = datetime.datetime.utcnow()
    db.commit()
    return study

def add_study_field(db: Session, study_id: int, field_data: ResearchStudyFieldCreate):
    """Add a dynamic field to a study (e.g., blood samples, questionnaires, etc.)"""
    db_field = ResearchStudyField(
        study_id=study_id,
        field_name=field_data.field_name,
        field_type=field_data.field_type,
        is_required=field_data.is_required
    )
    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return db_field

def update_study_field(db: Session, field_id: int, update_data: ResearchStudyFieldCreate):
    field = db.query(ResearchStudyField).filter(ResearchStudyField.id == field_id).first()
    if not field:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(field, key, value)
    db.commit()
    db.refresh(field)
    return field

def remove_study_field(db: Session, field_id: int):
    field = db.query(ResearchStudyField).filter(ResearchStudyField.id == field_id).first()
    if not field:
        return None
    db.delete(field)
    db.commit()
    return True

def list_study_fields(db: Session, study_id: int):
    return db.query(ResearchStudyField).filter(ResearchStudyField.study_id == study_id).all()

# Optionally: manage filled responses for studies

def create_study_response(db: Session, response_data: ResearchStudyResponseCreate):
    db_response = ResearchStudyResponse(
        study_id=response_data.study_id,
        patient_id=response_data.patient_id,
        filled_out_by=response_data.filled_out_by,
        created_by=response_data.created_by
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)

    # Insert individual field responses
    for field_resp in response_data.field_responses:
        db_field_resp = ResearchStudyFieldResponse(
            response_id=db_response.id,
            field_id=field_resp.field_id,
            value=field_resp.value
        )
        db.add(db_field_resp)
    db.commit()
    return db_response
