# appointment.py
# ---- CRUD operations for Appointment Scheduling and Integration with Outlook ----

from sqlalchemy.orm import Session
from models.models import Appointment_Scheduling_and_Status, Appointment, Encounter, db
from schemas import AppointmentCreate, AppointmentUpdate
from calendar_widget.outlook import schedule_if_available, update_outlook_event, delete_outlook_event
from datetime import datetime, timedelta
from sqlalchemy import or_, and_


def create_appointment(patient_id, provider_id, start_time, end_time, created_by):
    # Create encounter first
    encounter = Encounter(
        patient_id=patient_id,
        provider_id=provider_id,
        start_time=start_time,
        end_time=end_time,
        created_by=created_by,
        updated_by=created_by,
        created_date=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(encounter)
    db.session.flush()  # so encounter.id is generated

    appointment = Appointment(
        patient_id=patient_id,
        provider_id=provider_id,
        scheduled_start=start_time,
        scheduled_end=end_time,
        encounter_id=encounter.id,
        created_by=created_by,
        updated_by=created_by,
        created_date=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(appointment)
    db.session.commit()
    return appointment

def update_appointment(appointment_id, start_time, end_time, updated_by):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return None

    appointment.scheduled_start = start_time
    appointment.scheduled_end = end_time
    appointment.updated_by = updated_by
    appointment.updated_at = datetime.utcnow()

    # Also update encounter times if needed
    if appointment.encounter:
        appointment.encounter.start_time = start_time
        appointment.encounter.end_time = end_time
        appointment.encounter.updated_by = updated_by
        appointment.encounter.updated_at = datetime.utcnow()

    db.session.commit()
    return appointment

def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return False

    # Also delete linked encounter if you want
    if appointment.encounter:
        db.session.delete(appointment.encounter)

    db.session.delete(appointment)
    db.session.commit()
    return True




def get_appointment_by_id(db: Session, appointment_id: int):
    return db.query(Appointment_Scheduling_and_Status).filter_by(id=appointment_id).first()


def get_appointments_by_mrn(db: Session, mrn: str):
    return db.query(Appointment_Scheduling_and_Status).filter_by(mrn=mrn).all()


def get_appointments_by_provider(db: Session, provider: str):
    return db.query(Appointment_Scheduling_and_Status).filter_by(provider=provider).all()


def get_appointments_by_date_range(db: Session, start_date: datetime, end_date: datetime):
    return db.query(Appointment_Scheduling_and_Status).filter(
        and_(
            Appointment_Scheduling_and_Status.appointment_scheduled_start >= start_date,
            Appointment_Scheduling_and_Status.appointment_scheduled_end <= end_date,
        )
    ).all()


def search_appointments(db: Session, query: str):
    return db.query(Appointment_Scheduling_and_Status).filter(
        or_(
            Appointment_Scheduling_and_Status.mrn.ilike(f"%{query}%"),
            Appointment_Scheduling_and_Status.provider.ilike(f"%{query}%"),
            Appointment_Scheduling_and_Status.research_protocol.ilike(f"%{query}%"),
            Appointment_Scheduling_and_Status.scheduled_by.ilike(f"%{query}%")
        )
    ).all()


def get_all_appointments(db: Session):
    return db.query(Appointment_Scheduling_and_Status).all()


def sync_outlook_events_to_db(db: Session, days_ahead: int = 30):
    """
    Optional: Pull upcoming Outlook events and compare against DB for audit/sync.
    """
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=days_ahead)
    events = get_outlook_events(start_date, end_date)

    synced = []
    for event in events:
        subject = event.get("subject")
        start = datetime.fromisoformat(event['start']['dateTime'])
        end = datetime.fromisoformat(event['end']['dateTime'])

        existing = db.query(Appointment_Scheduling_and_Status).filter_by(
            appointment_scheduled_start=start,
            appointment_scheduled_end=end,
        ).first()

        if not existing:
            db_event = Appointment_Scheduling_and_Status(
                mrn=subject.split(" ")[2] if subject else "UNKNOWN",
                provider="Imported",
                appointment_scheduled_start=start,
                appointment_scheduled_end=end,
                research_protocol="Imported",
                scheduled_by="Outlook Sync",
            )
            db.add(db_event)
            synced.append(db_event)

    db.commit()
    return synced
