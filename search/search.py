# search/search.py

from utils.fuzzy_search_utils import fuzzy_match

class Search:
    """
    General-purpose search class for fuzzy and exact matching in a pandas DataFrame.
    """
    def __init__(self, df, threshold=70):
        self.df = df
        self.threshold = threshold

    def search(self, **criteria):
        exact_matches = []
        fuzzy_matches = []

        for attr, value in criteria.items():
            if value:
                exact = self._exact_match(attr, value)
                if exact:
                    exact_matches.extend(exact)
                else:
                    fuzzy = self._fuzzy_match(attr, value)
                    fuzzy_matches.extend(fuzzy)

        return (sorted(set(exact_matches), key=lambda x: x[0], reverse=True)
                if exact_matches else
                sorted(set(fuzzy_matches), key=lambda x: x[0], reverse=True))

    def _exact_match(self, attr, value):
        matches = self.df[self.df[attr] == value].to_dict(orient='records')
        return [(100, match) for match in matches] if matches else []

    def _fuzzy_match(self, attr, value):
        candidates = self.df[attr].astype(str).dropna().tolist()
        fuzzy_results = fuzzy_match(value, candidates, threshold=self.threshold, multiple=True)

        return [
            (score, row)
            for match_str, score in fuzzy_results
            if score >= self.threshold
            for _, row in self.df[self.df[attr] == match_str].iterrows()
        ]


class GreekAwareSearch(Search):
    """
    Extends Search to intelligently choose Greek or Latin name columns.
    """
    def search_names(self, first_name=None, last_name=None, prefix=""):
        criteria = {}

        if first_name:
            first_field = f"{prefix}First_name_gr" if is_greek(first_name) else f"{prefix}First_name"
            criteria[first_field] = first_name

        if last_name:
            last_field = f"{prefix}Last_name_gr" if is_greek(last_name) else f"{prefix}Last_name"
            criteria[last_field] = last_name

        return self.search(**criteria)
