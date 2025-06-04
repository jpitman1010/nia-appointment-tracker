# appointment.py
# ---- CRUD operations for Appointment Scheduling and Integration with Outlook ----

from sqlalchemy.orm import Session
from models import Appointment_Scheduling_and_Status
from schemas import AppointmentCreate, AppointmentUpdate
from outlook import schedule_if_available, get_outlook_events
from datetime import datetime, timedelta
from sqlalchemy import or_, and_


def create_appointment(db: Session, appointment_data: AppointmentCreate):
    """
    Create a new appointment and attempt to schedule in Outlook if available.
    """
    subject = f"Appointment for {appointment_data.mrn} ({appointment_data.research_protocol})"
    start_time = appointment_data.appointment_scheduled_start
    end_time = appointment_data.appointment_scheduled_end

    # Check Outlook calendar for availability
    outlook_event = schedule_if_available(
        subject=subject,
        start_time=start_time,
        end_time=end_time,
        body=f"Scheduled by: {appointment_data.scheduled_by}\nProvider: {appointment_data.provider}",
    )

    # Proceed with database insert regardless of Outlook result
    db_appointment = Appointment_Scheduling_and_Status(
        mrn=appointment_data.mrn,
        provider=appointment_data.provider,
        appointment_scheduled_start=start_time,
        appointment_scheduled_end=end_time,
        research_protocol=appointment_data.research_protocol,
        scheduled_by=appointment_data.scheduled_by,
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def update_appointment(db: Session, appointment_id: int, update_data: AppointmentUpdate):
    appointment = db.query(Appointment_Scheduling_and_Status).filter_by(id=appointment_id).first()
    if not appointment:
        return None

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(appointment, field, value)
    db.commit()
    db.refresh(appointment)
    return appointment


def delete_appointment(db: Session, appointment_id: int):
    appointment = db.query(Appointment_Scheduling_and_Status).filter_by(id=appointment_id).first()
    if appointment:
        db.delete(appointment)
        db.commit()
    return appointment


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
