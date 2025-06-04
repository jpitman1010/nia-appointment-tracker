# fuzzy_search_utils.py

from fuzzywuzzy import fuzz
from fuzzywuzzy import process as fuz_proc
import pandas as pd

def fuzzy_match(input_str, choices, threshold=70, multiple=False):
    """
    Finds the closest match(es) from a list of choices using fuzzy matching.

    Args:
        input_str (str): The string to search for.
        choices (list): List of candidate strings.
        threshold (int): Minimum score (0–100) to consider a match.
        multiple (bool): Whether to return multiple results or just the best match.

    Returns:
        list of tuples or tuple: Matched values and their scores.
    """
    if not input_str or not choices:
        return [] if multiple else None

    if multiple:
        matches = fuz_proc.extract(input_str, choices, scorer=fuzz.ratio)
        return [(match, score) for match, score in matches if score >= threshold]

    best_match = fuz_proc.extractOne(input_str, choices, scorer=fuzz.ratio)
    return best_match if best_match and best_match[1] >= threshold else None

def generalized_fuzzy_search(df, criteria, threshold=70):
    """
    Perform fuzzy search across a DataFrame based on a dictionary of attribute-value criteria.

    Args:
        df (pd.DataFrame): DataFrame to search.
        criteria (dict): Keys are column names, values are strings to match.
        threshold (int): Minimum score to consider a match.

    Returns:
        list of tuples: (score, matched row as dict)
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Expected a pandas DataFrame")

    matches = []

    for attr, value in criteria.items():
        if attr not in df.columns:
            continue

        attr_values = df[attr].astype(str).dropna().tolist()
        fuzzy_results = fuzzy_match(value, attr_values, threshold=threshold, multiple=True)

        for match_str, score in fuzzy_results:
            matched_rows = df[df[attr] == match_str].to_dict(orient="records")
            for row in matched_rows:
                matches.append((score, row))

    return sorted(matches, key=lambda x: x[0], reverse=True)
