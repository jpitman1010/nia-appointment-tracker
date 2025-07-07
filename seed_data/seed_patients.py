from datetime import datetime
import os
import sys
# Adjust path to import app and db correctly if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crud.patient import create_patient, Patient, db
from models.models import db, Patient
from server import app
from sqlalchemy_continuum import versioning_manager


def seed_patients():
    
    patients_data = [
        {
            "mrn": "MRN001",
            "fname": "Elika",
            "lname": "Papadopoulos",
            "greek_fname": "Ελίκα",
            "greek_lname": "Παπαδόπουλος",
            "dob": datetime(1985, 6, 15),
            "place_of_birth": "Athens",
            "sex": "Female",
            "handedness": "Right",
            "race": "Greek",
            "race_subtype": None,
            "fathers_name": "Nikos",
            "mothers_name": "Maria",
            "phone": "2101234567",
            "surrogate_phone": None,
            "surrogate_relationship": None,
            "address": "Athens, Greece",
            "email": "elika@example.com",
            "amka": "12345678901"
        },
        {
            "mrn": "MRN002",
            "fname": "Elina",
            "lname": "Papadopoulos",
            "greek_fname": "Ελίνα",
            "greek_lname": "Παπαδόπουλος",
            "dob": datetime(1985, 6, 15),  # Same DOB as above
            "place_of_birth": "Athens",
            "sex": "Female",
            "handedness": "Right",
            "race": "Greek",
            "race_subtype": None,
            "fathers_name": "Nikos",
            "mothers_name": "Maria",
            "phone": "2101234568",
            "surrogate_phone": None,
            "surrogate_relationship": None,
            "address": "Athens, Greece",
            "email": "elina@example.com",
            "amka": "12345678902"
        },
        {
            "mrn": "MRN003",
            "fname": "Elika",
            "lname": "Georgiou",
            "greek_fname": "Ελίκα",
            "greek_lname": "Γεωργίου",
            "dob": datetime(1990, 8, 20),
            "place_of_birth": "Thessaloniki",
            "sex": "Female",
            "handedness": "Right",
            "race": "Greek",
            "race_subtype": None,
            "fathers_name": "George",
            "mothers_name": "Anna",
            "phone": "2310234567",
            "surrogate_phone": None,
            "surrogate_relationship": None,
            "address": "Thessaloniki, Greece",
            "email": "elika.g@example.com",
            "amka": "12345678903"
        },
        # Add 17 more with some repeating first names, DOBs, phones, etc.
        {
            "mrn": "MRN004",
            "fname": "Nikos",
            "lname": "Papadopoulos",
            "greek_fname": "Νίκος",
            "greek_lname": "Παπαδόπουλος",
            "dob": datetime(1975, 2, 10),
            "place_of_birth": "Athens",
            "sex": "Male",
            "handedness": "Right",
            "race": "Greek",
            "race_subtype": None,
            "fathers_name": "Dimitris",
            "mothers_name": "Maria",
            "phone": "2101234569",
            "surrogate_phone": None,
            "surrogate_relationship": None,
            "address": "Athens, Greece",
            "email": "nikos.p@example.com",
            "amka": "12345678904"
        },
        {
            "mrn": "MRN005",
            "fname": "Niko",
            "lname": "Georgiou",
            "greek_fname": "Νίκο",
            "greek_lname": "Γεωργίου",
            "dob": datetime(1975, 2, 10),
            "place_of_birth": "Thessaloniki",
            "sex": "Male",
            "handedness": "Left",
            "race": "Greek",
            "race_subtype": None,
            "fathers_name": "George",
            "mothers_name": "Anna",
            "phone": "2310234568",
            "surrogate_phone": None,
            "surrogate_relationship": None,
            "address": "Thessaloniki, Greece",
            "email": "niko.g@example.com",
            "amka": "12345678905"
        },
        # 15 more entries, similar structure, varying names and DOBs
    ]
        # Add more dummy patients to make total 20
        # For brevity, here's a loop to add similar dummy data with variations
    base_dobs = [datetime(1980,1,1), datetime(1990,5,15), datetime(1975,7,30)]
    
    for i in range(6, 21):
        patient = {
            "mrn": f"MRN{str(i).zfill(3)}",
            "fname": f"TestName{i%5}",        # repeats every 5 patients
            "lname": f"TestLast{i%7}",        # repeats every 7 patients
            "greek_fname": f"Δοκιμή{i%5}",
            "greek_lname": f"Επώνυμο{i%7}",
            "dob": base_dobs[i % 3],
            "place_of_birth": "Athens",
            "sex": "Female" if i % 2 == 0 else "Male",
            "handedness": "Right",
            "race": "Greek",
            "race_subtype": None,
            "fathers_name": "FatherName",
            "mothers_name": "MotherName",
            "phone": f"2101000{i:04d}",
            "surrogate_phone": None,
            "surrogate_relationship": None,
            "address": "Athens, Greece",
            "email": f"test{i}@example.com",
            "amka": f"9000000000{i:02d}"
        }
        patients_data.append(patient)

    with app.app_context():
        # Disable versioning temporarily
        versioning_manager.options['versioning'] = False

        for pdata in patients_data:
            exists = db.session.query(Patient).filter_by(mrn=pdata['mrn']).first()
            if not exists:
                patient = create_patient(**pdata)
                print(f"Created patient: {patient.mrn} - {patient.fname} {patient.lname}")
            else:
                print(f"Patient with MRN {pdata['mrn']} already exists.")
        
        # Re-enable versioning if you want afterwards (optional)
        versioning_manager.options['versioning'] = True

if __name__ == "__main__":
    seed_patients()

