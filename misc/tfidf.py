import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


def get_tfidf_matches(in_string, lookup, ngram_length=3, k_matches=3):
    """Matches a string against a number of other strings via tfidf.

    Parameters
        ----------
        in_string : string
            String that should be matched against the strings in lookup.

        lookup : iterable
            An iterable which generates either str, unicode or file objects.

        ngram_length : integer
            Length of ngrams.

        k_matches : integer
            Number of matches

        Returns
        -------
        : dict
            A dictionary with the k best matches. Keys are the indices of the
            lookup, values are the calculated distances. The lower the distance,
            the better the match.
    """
    vectorizer = TfidfVectorizer(
        analyzer=lambda string, n=ngram_length: zip(*[string[i:] for i in range(n)])  # type: ignore
    )
    tf_idf_lookup = vectorizer.fit_transform(lookup)

    nbrs = NearestNeighbors(n_neighbors=k_matches, n_jobs=-1, metric="cosine").fit(
        tf_idf_lookup
    )
    print(nbrs)
    tf_idf_original = vectorizer.transform([in_string])
    distances, lookup_indices = nbrs.kneighbors(tf_idf_original)

    return dict(zip(lookup_indices[0], distances[0]))


test = pd.DataFrame()
test["names"] = [
    "alphabet",
    "annegret",
    "alpha",
    "beta",
    "arbeit",
    "aloe vera",
    "anakin",
    "alphons",
    "alpha ville",
]

print(get_tfidf_matches("alph", test.loc[:, "names"], 3, 4))
