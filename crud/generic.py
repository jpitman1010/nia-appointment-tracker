# generic_search.py

from utils.fuzzy_search_utils import generalized_fuzzy_search
import pandas as pd

def search_entity(df: pd.DataFrame, search_terms: dict, threshold: int = 75):
    """
    Generic search function for any entity using fuzzy matching.

    Args:
        df (pd.DataFrame): The DataFrame containing entity data.
        search_terms (dict): Keys are column names, values are search strings.
        threshold (int): Minimum score to be considered a match.

    Returns:
        List of (score, row_dict) tuples sorted by match score.
    """
    return generalized_fuzzy_search(df, search_terms, threshold)

# Example specialized helpers for convenience:
def search_patients(dem_df: pd.DataFrame, terms: dict, threshold: int = 75):
    return search_entity(dem_df, terms, threshold)

def search_staff(staff_df: pd.DataFrame, terms: dict, threshold: int = 75):
    return search_entity(staff_df, terms, threshold)

def search_clinicians(clin_df: pd.DataFrame, terms: dict, threshold: int = 75):
    return search_entity(clin_df, terms, threshold)

def search_appointments(appt_df: pd.DataFrame, terms: dict, threshold: int = 75):
    return search_entity(appt_df, terms, threshold)
