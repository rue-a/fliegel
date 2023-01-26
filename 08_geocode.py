import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


def get_tfidf_matches(in_string, lookup, ngram_length=3, k_matches=3) -> dict:
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
    tf_idf_original = vectorizer.transform([in_string])
    distances, lookup_indices = nbrs.kneighbors(tf_idf_original)

    return dict(zip(lookup_indices[0], distances[0]))


dtypes = {"admin_level_2": object, "admin_level_1": object}
fliegel = pd.read_csv("interim/fliegel_prepared.csv", dtype=dtypes)

# manual assignments
rename = {}
rename["Acapulco"] = "Acapulco de Juarez"
rename["Miami Bay"] = "Maumee Bay"
fliegel.at[
    fliegel[fliegel["place_name"] == "Cape of Good Hope"].index.item(), "admin_level_0"
] = "ZA"
fliegel.at[
    fliegel[fliegel["place_name"] == "Berbice"].index.item(), "admin_level_0"
] = "GY"


dtypes = {"admin2 code": object, "admin1 code": object}
geonames = pd.read_csv("geonames/geonames_prepared.csv", low_memory=False, dtype=dtypes)

fliegel["latitude"] = None
fliegel["longitude"] = None
fliegel["matched_name"] = None

# fliegel_without_meta = fliegel[pd.isna(fliegel["admin_level_2"])][
#     pd.isna(fliegel["admin_level_1"])
# ][pd.isna(fliegel["admin_level_0"])][pd.isna(fliegel["feature_type"])]

# fliegel_with_meta = fliegel.drop(fliegel_without_meta.index)

# print(fliegel_with_meta)

for index, row in fliegel.iterrows():
    print(list(row))
    place_name = row["place_name"]
    if place_name in rename.keys():
        place_name = rename[place_name]
    sub_geonames = geonames
    information = {}
    if not pd.isna(row["admin_level_2"]):
        information["admin2 code"] = [row["admin_level_2"]]
    if not pd.isna(row["admin_level_1"]):
        information["admin1 code"] = [row["admin_level_1"]]
    if not pd.isna(row["admin_level_0"]):
        information["country code"] = [row["admin_level_0"]]
    if not pd.isna(row["feature_type"]):
        information["feature class"] = [row["feature_type"]]
    # if no admin info is given, assume that place is in CA or US
    if (
        "admin2 code" not in information.keys()
        and "admin1 code" not in information.keys()
        and "country code" not in information.keys()
    ):
        information["country code"] = ["US", "CA"]
    for key, val in information.items():
        sub_geonames = sub_geonames.loc[sub_geonames[key].isin(val)]
    # matched name has to begin with same letter
    sub_geonames_backup = sub_geonames
    sub_geonames = sub_geonames[sub_geonames["asciiname"].str.startswith(place_name[0])]
    sub_geonames = sub_geonames.reset_index()
    if len(sub_geonames) > 0:
        best_match_index, best_match_distance = next(
            iter(
                # ngram legth has to be <= length shortest word (here: york)
                get_tfidf_matches(
                    place_name, sub_geonames["asciiname"], ngram_length=4, k_matches=1
                ).items()
            )
        )
        if best_match_distance < 0.3:
            lat = sub_geonames.loc[best_match_index, "latitude"]
            lon = sub_geonames.loc[best_match_index, "longitude"]
            matched_name = sub_geonames.loc[best_match_index, "asciiname"]
            fliegel.at[index, "latitude"] = lat
            fliegel.at[index, "longitude"] = lon
            fliegel.at[index, "matched_name"] = matched_name
        else:
            for place_name in eval(row["alternate_names"]):
                if "also" in place_name:
                    place_name = place_name.split("also")[1].strip()
                print(place_name)
                sub_geonames = sub_geonames_backup
                sub_geonames = sub_geonames[
                    sub_geonames["asciiname"].str.startswith(place_name)
                ]
                sub_geonames = sub_geonames.reset_index()
                if len(sub_geonames) > 0:
                    best_match_index, best_match_distance = next(
                        iter(
                            # ngram legth has to be <= length shortest word (here: york)
                            get_tfidf_matches(
                                place_name,
                                sub_geonames["asciiname"],
                                ngram_length=4,
                                k_matches=1,
                            ).items()
                        )
                    )
                    if best_match_distance < 0.3:
                        lat = sub_geonames.loc[best_match_index, "latitude"]
                        lon = sub_geonames.loc[best_match_index, "longitude"]
                        matched_name = sub_geonames.loc[best_match_index, "asciiname"]
                        fliegel.at[index, "latitude"] = lat
                        fliegel.at[index, "longitude"] = lon
                        fliegel.at[index, "matched_name"] = matched_name
                        print(f"matched synonym '{place_name}'")
                        break


fliegel.to_csv("interim/fliegel_geocoded.csv", index=False)
