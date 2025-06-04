"""Server operations. CRUD = create,read,update,delete"""

from models.models import Staff, Provider, Patient, Appointment_Scheduling_and_Status, Research_Studies, db, connect_to_db, Encounter
import psycopg2
import config
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, Boolean, text


def create_staff(email, password, fname, lname, role, enabled):
    """Create and return a new staff."""

    staff = Staff(email=email, password=password, fname=fname,
                  lname=lname, role=role, enabled=enabled)

    db.session.add(staff)
    db.session.commit()

    return staff


def get_staff_id(email):
    """Return the staff object by ID"""

    staff_id = db.session.query(Staff.id).filter_by(email=email).first()

    return staff_id[0]


def get_staff_fname(email):
    """get staff's fname for return users"""
    fname = db.session.query(Staff.fname).filter_by(email=email).first()

    return fname[0]


def get_staff_name(email):
    """get full name of staff member"""
    fname = db.session.query(Staff.fname).filter_by(email=email).first()
    lname = db.session.query(Staff.lname).filter_by(email=email).first()
    staff_name = fname[0] + " " + lname[0]

    return staff_name


def check_if_valid_user(email):
    """Return staff email from registration"""

    user_exists_check = db.session.query(Staff).filter_by(email=email).first()

    return not not user_exists_check


def password_check(email, password):
    """verify that login information matches database of registered staff"""

    valid_password = db.session.query(
        Staff).filter_by(password=password).first()

    return not not valid_password


def create_patient(mrn, fname, lname, Greek_fname, Greek_lname, dob, place_of_birth, sex, handedness, race, race_subtype, fathers_name, mothers_name, phone, surrogate_phone, surrogate_relationship, address, email, amka):
    """Create and return a new patient."""

    patient = Patient(mrn=mrn, fname=fname, lname=lname, Greek_fname=Greek_fname, Greek_lname=Greek_lname,
                      dob=dob, place_of_birth=place_of_birth, sex=sex, handedness=handedness, race=race, race_subtype=race_subtype, fathers_name=fathers_name, mothers_name=mothers_name, phone=phone, surrogate_phone=surrogate_phone, surrogate_relationship=surrogate_relationship, address=address, email=email, amka=amka)

    db.session.add(patient)
    db.session.commit()

    print(patient)

    return patient


def get_all_pateints():
    """get all patient objects for search engine"""
    patient_list = []
    # patient_list = db.session.query(Patient)
    # for patient in patient_list:
    #     print(patient.__repr__)
    patient = db.session.query(Patient).filter_by(id=1).first()
    print(patient)
    return patient_list


def search_by_mrn(mrn):
    """search database for patient via mrn return a patient object"""

    patient = db.session.query(Patient).filter_by(mrn=mrn).first()

    return patient


def search_by_latin_name(fname, lname):
    """search for patient by first and last name return patient object"""

    patient = db.session.query(Patient).filter_by(
        fname=fname, lname=lname).first()

    return patient


def search_by_greek_name(Greek_fname, Greek_lname):
    """search for patient by first and last name return patient object"""

    patient = db.session.query(Patient).filter_by(
        Greek_fname=Greek_fname, Greek_lname=Greek_lname).all()

    return patient


def search_by_dob(dob):
    """search for patient by dob, return list of patients with this dob"""

    patients_by_dob = db.session.query(Patient).filter_by(dob=dob).all()

    return patients_by_dob


def check_if_patient_exists(lname, dob, mrn):
    """Check to see if patient exists in database already"""

    patient_exists_check = db.session.query(Patient).filter_by(
        dob=dob, lname=lname, mrn=mrn).first()

    print(patient_exists_check)

    return not not patient_exists_check

def create_encounter_type(encounter_name, encounter_duration, duration_metric, encounter_type):
    """creates a new encounter type"""
    encounter = Encounter(encounter_name = encounter_name, encounter_duration = encounter_duration, duration_metric = duration_metric, encounter_type = encounter_type)
    db.session.add(encounter)
    db.session.commit()
    return encounter


def get_report_types():
    """returns a list of all classes in Model.py for searchable table options"""

    conn = psycopg2.connect(host='localhost', dbname='mySchema',
                            user='myUserName', password='myPassword')
    cursor = conn.cursor()

    cursor.execute("""SELECT relname FROM pg_class WHERE relkind='r'
                  AND relname !~ '^(pg_|sql_)';""")  # "rel" is short for relation.

    tables = [i[0] for i in cursor.fetchall()]  # A list() of tables.
    print(tables)

    return tables


# __________________________________________
# research protocol

# ability to create table and columns
# select/identify anchor appointment (T)
# ability to set expected (E) range for appointments beyond appointment T
# ability to set wiggle (W) room for appointment that fall outside of expected completion dates
# other requirements needing to be satisfied, identified as complete by inputting completion date
# way to indicate frequency of things like questionnaires, labs, bio-samples, MRI's, PSG, EEG, etc...
# require certain elements be entered in for every study to ensure report and search features are usable and don't break the code.
# Table name must == Name of Study

# reports of how many have finished what
# reports of who has upcoming appointment due in the next month, 3 months, etc...
# reports of

# server.py will need to collect values from input for anchor appointment
# and each follow up appointment acceptable range for completing the appointment, create
# dates for a range of time the appointment can occur, so each appt will come through as a dict
# taking appointment name/type and first appointment will be T (anchor appointment)
# so dict will be requirements kwargs =
#  {apts: {appt1: dateTime, appt2: x days/months past appt 1, appt3: x days/months past appt 1, etc...
# [earliest date from appt1, latest acceptable date from appt 1], etc...}, paperwork: {}, tests:{}, bio-samples: {}

def create_table(study_name):
    """ create tables in the PostgreSQL database"""
    print('crud study name for creating table/class for research protocol === ', study_name)

    table_name = study_name.title()

    commands = f"""
        CREATE TABLE {table_name} (
                id SERIAL PRIMARY KEY
                )"""

    conn = psycopg2.connect(
        host='127.0.0.1', database='NIA_Appointment_Tracker')
    cur = conn.cursor()
    try:
        # create table one by one
        cur.execute(commands)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return


def add_columns_to_table(protocol_name, self,  **kwargs):
    """add appointments/tests/required paperwork/bio-samples to research protocol table"""

    print(self)
    # table_name = kwargs['table_name']
    # connect to the PostgreSQL server
    table_name = protocol_name

    conn = psycopg2.connect(
        host='127.0.0.1', database='NIA_Appointment_Tracker')
    cur = conn.cursor()

    for column_header in self.kwargs:
        cur.execute(
            'ALTER TABLE {table_name} ADD {column_header} {self.kwargs[column_header]}')
        print('crud fcn to add columns to protocol table => ',
              f"Alter TABLE {table_name} ADD {column_header} {self.kwargs[column_header]}")

    # need to backref this to patient table to get this to work properly

    # for column in self.keys():
    #     cur.execute('ALTER TABLE %s ADD COLUMN %s column' %
    #                 (table_name, value))

    print('self.keys -== ', self.keys())

    # for paperwork in self['ppw']:
    #     cur.execute('ALTER TABLE %s ADD COLUMN %s date' %
    #                 (table_name, paperwork))
    # for lab in self['labs']:
    #     cur.execute('ALTER TABLE %s ADD COLUMN %s date' %
    #                 (table_name, lab))
    # for test in self['tests']:
    #     cur.execute('ALTER TABLE %s ADD COLUMN %s date' %
    #                 (table_name, test))
    # for bio_sample in self['biosamples']:
    #     cur.execute('ALTER TABLE %s ADD COLUMN %s date' %
    #                 (table_name, bio_sample))
    # for additional in self['additionals']:
    #     cur.execute('ALTER TABLE %s ADD COLUMN %s date' %
    #                 (table_name, additional))

    cur.close()
    conn.commit()
    print('added columns!!')

    return


def add_a_column_to_table(table_name, column_name, data_type):
    """add a column to a table"""

    conn = psycopg2.connect(
        host='127.0.0.1', database='NIA_Appointment_Tracker')
    cur = conn.cursor()
    cur.execute('ALTER TABLE %s ADD COLUMN %s {data_type}' % (
        table_name, column_name))

    cur.close()
    conn.commit()

    return


def add_research_study_to_Research_Study_table(name_of_study, p_i, research_coordinator, criteria_entered_by, start_of_study_date, end_of_study_date):
    """add research study to database"""

    study = f'Research)studies(name_of_study = {name_of_study}, p_i = {p_i}, research_coordinator = {research_coordinator}, criteria_entered_by = {criteria_entered_by}, start_of_study_date = {start_of_study_date}, end_of_study_date = {end_of_study_date}'
    print('add_research_study_to_Research_Study_table ===', study)
    # study = Research_Studies(name_of_study=name_of_study, p_i=p_i, research_coordinator=research_coordinator,
    #                          criteria_entered_by=criteria_entered_by, start_of_study_date=start_of_study_date, end_of_study_date=end_of_study_date)
    # db.session.add(study)
    # db.session.commit()

    return study


# reports

def find_all_research_projects():
    """return a list of all research studies/tables in the database"""

    research_projects = db.session.query(Research_Studies).all()

    list_of_research_projects = []

    for object in research_projects:
        study_name = object['name']
        list_of_research_projects.append(study_name)

    print(list_of_research_projects)

    return list_of_research_projects


def study_by_PI(p_i):
    """find all research studies based on who is the PI"""

    research_by_PI = db.session.query(
        Research_Studies).filter_by(p_i=p_i).all()

    return research_by_PI


def active_research_studies():
    """find all research studies that are actively going as of today's date"""
    date = "09-30-22"  # get today's date with python

    active_studies = db.session.query(Research_Studies).filter_by(
        end_of_study_date > date).all()

    return active_studies


def get_patient_mrn(patient_id):
    """get the patient's mrn by id"""

    mrn = db.session.query("Patient").filter_by(id=patient_id).first()

    return mrn


def get_protocol_title_by_patient_id(patient_id):
    """Look up patient by pt id, find which research protocol(s) they are in and return list of name(s) of protocol"""
    mrn = get_patient_mrn(patient_id)
    research_study_list = find_all_research_projects()
    list_of_protocols_for_patient = []

    if research_study_list != None:
        for study in research_study_list:
            study_pt_is_in = db.session.query(study).filter_by(mrn=mrn).first()
            list_of_protocols_for_patient.append(study_pt_is_in)
        return list_of_protocols_for_patient
    else:
        return "Clinic Patient"


def get_task_list(study):
    """get list of tasks within a protocol by patient id"""
#     SELECT
#       column_name,
#       data_type
#     FROM
#       information_schema.columns
#     WHERE
#       table_name = 'table_name';

    task_list = db.session.query(
        study.information_schema.columns).column_name.all()
    print(task_list)
    return task_list


def get_research_protocol_id(study):
    """get research protocol id using patient id"""
    protocol_id = db.session.query(study.id).first()
    return protocol_id


def get_task_object_list(research_protocol_id):
    """get task object list based on research protocol's id"""

    return


def query_research_studies_by_mrn(mrn):
    """query all research studies to see if a specific patient is a participant"""
    projects_to_query = find_all_research_projects()

    studies_participating_in = []
    for project in projects_to_query:
        table_name = project['name'].title()
        mrn_search = db.session.query(table_name).filter_by(mrn=mrn).first()
        if mrn_search:
            studies_participating_in.append(table_name)

    return studies_participating_in


def query_specific_study_for_participants_list(study_name):
    """query a specific research study to get a list of patient objects"""
    # need to test this, it will likely break/not work
    participants = db.session.query(study_name).find(mrn).all()

    return participants


def schedule_appointment(mrn, provider, appointment_scheduled_start, appointment_scheduled_end, research_protocol, email):
    """schedule an appointment"""
    #  mrn = db.Column(db.String,)
    # provider = db.Column(db.String,)
    # appointment_scheduled_start = db.Column(db.DateTime,)
    # appointment_scheduled_end = db.Column(db.DateTime,)
    # appointment_completed_date = db.Column(db.DateTime,)
    # research_protocol = db.Column(db.String,)  # backref to protocol
    # scheduled_by = db.Column(db.String)  # backref to user

    scheduled_by = get_staff_name(email=email)
    schedule_appointment = Appointment_Scheduling_and_Status(mrn=mrn, provider=provider, appointment_scheduled_start=appointment_scheduled_start,
                                                             appointment_scheduled_end=appointment_scheduled_end, research_protocol=research_protocol, scheduled_by=scheduled_by)

    db.session.add(schedule_appointment)
    db.session.commit()

    return schedule_appointment


def get_to_do_list(mrn):
    """get a to do list for the patient, includes completed and incomplete items to complete for 
    all research protocols patient is a part of."""

    studies = query_research_studies_by_mrn(mrn)

    task_list = []

    for study in studies:
        task_list.append(get_task_list(study))

    return task_list


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    # create_table("Cool_Research_Study")
    kwargs = {'table_name': "Cool_Research_Study", 'appts': ['apt1', 'apt2', 'apt3', 'apt4'], 'ppw': ['ess', 'isi', 'cognitive_something'], 'labs': [
        'feritin', 'blood_gas'], 'tests': ['eeg', 'psg', 'mslt'], 'biosamples': ['hair', 'plasma_and_serum', 'biopsy'], 'additionals': ['other', 'stuff']}
    add_columns_to_table(kwargs)