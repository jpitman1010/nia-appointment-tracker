# models.py
from sqlalchemy_continuum import make_versioned, versioning_manager
# Enable SQLAlchemy-Continuum versioning for GDPR compliance
make_versioned(user_cls=None)

import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey, Enum, Table
from sqlalchemy.dialects.postgresql import JSON  # Make sure to import this for JSON support


# Initialize DB
# ===========================================
db = SQLAlchemy()


def connect_to_db(flask_app, db_uri='postgresql:///NIA_Appointment_Tracker', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


# ===========================================
# Models with GDPR-Compliant Audit Fields
# ===========================================

# Association table between Staff and Roles

class Role(db.Model):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)  # e.g. 'physician'
    description = Column(String(255), nullable=True)

    # Permission flags - add or remove as needed
    can_prescribe = Column(Boolean, default=False)
    can_order_tests = Column(Boolean, default=False)
    can_manage_users = Column(Boolean, default=False)
    can_view_billing = Column(Boolean, default=False)
    can_view_research_data = Column(Boolean, default=False)
    can_schedule_appointments = Column(Boolean, default=False)
    # Add more as you identify...

    def __repr__(self):
        return f"<Role {self.name}>"

# Staff model:

staff_roles = db.Table(
    'staff_roles',
    db.Column('staff_id', db.Integer, db.ForeignKey('staff.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

class Staff(db.Model):
    __tablename__ = "staff"
    __versioned__ = {}

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    enabled = db.Column(db.Boolean, default=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String)
    deleted_at = db.Column(db.DateTime)
    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Replace role string with relationship
    roles = db.relationship('Role', secondary=staff_roles, backref=db.backref('staff_members', lazy='dynamic'))

    #roles = db.relationship('Role', secondary=staff_roles, backref='staff_members')

    def __repr__(self):
        role_names = [role.name for role in self.roles]
        return f"<Staff ID={self.id}, Name={self.fname} {self.lname}, Roles={role_names}, Email={self.email}>"

class Provider(db.Model):
    __tablename__ = "provider"
    __versioned__ = {}
    # GDPR: Includes audit trail fields for Article 30 compliance

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    type = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String)
    deleted_at = db.Column(db.DateTime)
    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Provider ID={self.id}, Name={self.fname} {self.lname}, Type={self.type}>"


class ProviderAvailability(db.Model):
    __tablename__ = "provider_availability"
    # Supporting provider scheduling. No sensitive data; no audit fields required.

    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey("provider.id"), nullable=False)
    day_of_week = db.Column(db.String, nullable=False)
    start_time = db.Column(db.String)
    end_time = db.Column(db.String)

    provider = db.relationship("Provider", backref="availability")


class Encounter(db.Model):
    __tablename__ = "encounter"
    __versioned__ = {}
    # GDPR: Encounter logs must be traceable (Article 30)

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey("provider.id"), nullable=False)
    encounter_name = db.Column(db.String)
    encounter_duration = db.Column(db.Integer)
    duration_metric = db.Column(db.String)
    encounter_type = db.Column(db.String)

    note_text = db.Column(db.Text)  # Raw full clinical note text
    structured_note = db.Column(JSON, default={})  # Parsed JSON structure for searching
    pdf_path = db.Column(db.String)  # File path to generated PDF (optional)

    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String)
    deleted_at = db.Column(db.DateTime)

    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    patient = db.relationship("Patient", backref="encounters")
    provider = db.relationship("Provider", backref="encounters")

    def __repr__(self):
        return f"<Encounter ID={self.id}, Patient={self.patient_id}, Provider={self.provider_id}, Type={self.encounter_type}>"

class ResearchStudy(db.Model):
    __tablename__ = "research_study"
    __versioned__ = {}
    # GDPR: Tracks personal data handling under research protocols (Articles 5, 30)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    principal_investigator = db.Column(db.String)
    coordinator = db.Column(db.String)
    criteria_entered_by = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String)
    deleted_at = db.Column(db.DateTime)
    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class ResearchStudyField(db.Model):
    __tablename__ = "research_study_field"
    # Defines structure of dynamic data fields; audit handled via parent

    id = db.Column(db.Integer, primary_key=True)
    study_id = db.Column(db.Integer, db.ForeignKey("research_study.id"), nullable=False)
    field_name = db.Column(db.String, nullable=False)
    field_type = db.Column(db.String, nullable=False)
    is_required = db.Column(db.Boolean, default=False)

    study = db.relationship("ResearchStudy", backref="fields")


class ResearchStudyResponse(db.Model):
    __tablename__ = "research_study_response"
    __versioned__ = {}
    # GDPR: Response records must be traceable for consent/audit review (Article 30)

    id = db.Column(db.Integer, primary_key=True)
    study_id = db.Column(db.Integer, db.ForeignKey("research_study.id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    filled_out_by = db.Column(db.String)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String)
    deleted_at = db.Column(db.DateTime)
    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    study = db.relationship("ResearchStudy", backref="responses")
    patient = db.relationship("Patient", backref="study_responses")


class ResearchStudyFieldResponse(db.Model):
    __tablename__ = "research_study_field_response"
    # Field-level responses; changes to values are tracked via parent link.

    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer, db.ForeignKey("research_study_response.id"), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey("research_study_field.id"), nullable=False)
    value = db.Column(db.String)

    response = db.relationship("ResearchStudyResponse", backref="field_answers")
    field = db.relationship("ResearchStudyField", backref="responses")


class Appointment(db.Model):
    __tablename__ = "appointment"
    __versioned__ = {}
    # GDPR: Time-sensitive clinical actions must be tracked (Article 30, 5)

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey("provider.id"), nullable=False)
    scheduled_start = db.Column(db.DateTime)
    scheduled_end = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)
    research_protocol = db.Column(db.String)
    scheduled_by = db.Column(db.String)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String)
    deleted_at = db.Column(db.DateTime)
    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    patient = db.relationship("Patient", backref="appointments")
    provider = db.relationship("Provider", backref="appointments")

    def __repr__(self):
        return f"<Appointment ID={self.id}, Patient={self.patient_id}, Provider={self.provider_id}, Start={self.scheduled_start}>"


class Patient(db.Model):
    __tablename__ = "patient"
    __versioned__ = {}
    # GDPR: Full data subject tracking — includes sensitive identifiers (Articles 5, 9, 30)

    id = db.Column(db.Integer, primary_key=True)
    mrn = db.Column(db.String, unique=True, nullable=False)
    greek_fname = db.Column(db.String)
    greek_lname = db.Column(db.String)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    dob = db.Column(db.DateTime)
    place_of_birth = db.Column(db.String)
    sex = db.Column(Enum('Male', 'Female', 'Other', name='sex_enum'))
    handedness = db.Column(Enum('Left', 'Right', 'Ambidextrous', name='hand_enum'))
    race = db.Column(db.String)
    race_subtype = db.Column(db.String)
    fathers_name = db.Column(db.String)
    mothers_name = db.Column(db.String)
    phone = db.Column(db.String)
    surrogate_phone = db.Column(db.String)
    surrogate_relationship = db.Column(db.String)
    address = db.Column(db.String)
    email = db.Column(db.String)
    amka = db.Column(db.String)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String)
    deleted_at = db.Column(db.DateTime)
    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Patient ID={self.id}, MRN={self.mrn}, Name={self.fname} {self.lname}>"


# ===============================
# Questionnaire Framework (Flexible)
# ===============================

class Questionnaire(db.Model):
    __tablename__ = "questionnaire"
    __versioned__ = {}
    # GDPR: Audit needed for any tools used in assessments (Article 30)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    version = db.Column(db.String, nullable=False)
    language = db.Column(db.String, nullable=False)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String)
    deleted_at = db.Column(db.DateTime)
    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Questionnaire {self.name} v{self.version} ({self.language})>"


class Question(db.Model):
    __tablename__ = "question"
    # Structural metadata, not subject to deletion tracing directly.

    id = db.Column(db.Integer, primary_key=True)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey("questionnaire.id"), nullable=False)
    question_code = db.Column(db.String, nullable=False)
    display_text = db.Column(db.String, nullable=False)
    order = db.Column(db.Integer)
    field_type = db.Column(db.String, nullable=False, default='text')  # e.g. text, radio, checkbox, number, select, textarea

    questionnaire = db.relationship("Questionnaire", backref="questions")

    def __repr__(self):
        return f"<Question {self.question_code}: {self.display_text[:30]}>"


class QuestionOption(db.Model):
    __tablename__ = "question_option"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    option_text = db.Column(db.String, nullable=False)
    option_value = db.Column(db.String)  # optional, for codes/values
    order = db.Column(db.Integer)        # optional ordering for options

    question = db.relationship("Question", backref="options")

    def __repr__(self):
        return f"<QuestionOption {self.option_text} for Question ID {self.question_id}>"

class QuestionnaireResponse(db.Model):
    __tablename__ = "questionnaire_response"
    __versioned__ = {}
    # GDPR: Questionnaire responses are personal data (Article 5, 30)

    id = db.Column(db.Integer, primary_key=True)
    mrn = db.Column(db.String, nullable=False)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey("questionnaire.id"), nullable=False)
    filled_out_by = db.Column(db.String)
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.String)
    deleted_at = db.Column(db.DateTime)
    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    questionnaire = db.relationship("Questionnaire", backref="responses")

    def __repr__(self):
        return f"<QuestionnaireResponse for {self.mrn} on {self.created_date}>"

class Response(db.Model):
    __tablename__ = "response"
    # Minimal data units — rely on parent audit trail for tracking

    id = db.Column(db.Integer, primary_key=True)
    response_set_id = db.Column(db.Integer, db.ForeignKey("questionnaire_response.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    answer = db.Column(db.String)

    questionnaire_response = db.relationship("QuestionnaireResponse", backref="answers")
    question = db.relationship("Question", backref="responses")

    def __repr__(self):
        return f"<Response q={self.question_id} a={self.answer}>"


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
