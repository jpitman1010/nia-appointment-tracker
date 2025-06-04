from models.models import Patient, db
from utils.fuzzy_search_utils import generalized_fuzzy_search
import pandas as pd

def search_patients(dem_df: pd.DataFrame, search_terms: dict, threshold: int = 75):
    """
    Search for patients using fuzzy matching.
    
    Args:
        dem_df (pd.DataFrame): The patient DataFrame.
        search_terms (dict): Dictionary like {"first_name": "Elika", "last_name": "Papadopoulos"}
        threshold (int): Fuzzy match threshold (default 75).

    Returns:
        List of (score, row_dict) tuples sorted by match score.
    """
    return generalized_fuzzy_search(dem_df, search_terms, threshold)



def create_patient(mrn, fname, lname, greek_fname, greek_lname, dob, place_of_birth,
                   sex, handedness, race, race_subtype, fathers_name, mothers_name,
                   phone, surrogate_phone, surrogate_relationship, address, email, amka):
    """Create and return a new patient."""
    patient = Patient(
        mrn=mrn,
        fname=fname,
        lname=lname,
        greek_fname=greek_fname,
        greek_lname=greek_lname,
        dob=dob,
        place_of_birth=place_of_birth,
        sex=sex,
        handedness=handedness,
        race=race,
        race_subtype=race_subtype,
        fathers_name=fathers_name,
        mothers_name=mothers_name,
        phone=phone,
        surrogate_phone=surrogate_phone,
        surrogate_relationship=surrogate_relationship,
        address=address,
        email=email,
        amka=amka
    )
    db.session.add(patient)
    db.session.commit()
    return patient


def search_by_mrn(mrn):
    """Search for a patient by MRN."""
    return db.session.query(Patient).filter_by(mrn=mrn).first()


def search_by_latin_name(fname, lname):
    """Search for a patient by first and last name (Latin characters)."""
    return db.session.query(Patient).filter_by(fname=fname, lname=lname).first()


def search_by_greek_name(greek_fname, greek_lname):
    """Search for a patient by Greek first and last name."""
    return db.session.query(Patient).filter_by(
        greek_fname=greek_fname, greek_lname=greek_lname
    ).all()


def search_by_dob(dob):
    """Return list of patients with the given DOB."""
    return db.session.query(Patient).filter_by(dob=dob).all()


def check_if_patient_exists(lname, dob, mrn):
    """Check if a patient already exists based on last name, DOB, and MRN."""
    return db.session.query(Patient).filter_by(
        lname=lname, dob=dob, mrn=mrn
    ).first() is not None
