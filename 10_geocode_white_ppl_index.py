import pandas as pd
import csv

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# find row with geoinformation by matching the against the qualified
# locations in fliegel_gazetteer.csv


fliegel_gazetteer = pd.read_csv("fliegel_gazetteer.csv").fillna("")

# TODO single place names first, then long

lookup = fliegel_gazetteer["place_name"]
lookup_long = lookup
for col in ["admin_level_2", "admin_level_1", "admin_level_0", "continent"]:
    lookup_long = lookup_long.str.cat(fliegel_gazetteer[col], sep=",")
for i, line in enumerate(lookup_long):
    while ",," in line:
        line = line.replace(",,", ",")
    line = line.strip(",").replace(",", ", ")
    lookup_long[i] = line
    if "," in line:
        place_name = line.split(",", 1)[0]
        appendix = line.split(",", 1)[1]
        if place_name in appendix:
            lookup_long[i] = appendix.strip()


vectorizer = TfidfVectorizer(
    analyzer=lambda string, n=5: zip(*[string[i:] for i in range(n)])  # type: ignore
)
tf_idf_lookup = vectorizer.fit_transform(lookup)
nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1, metric="cosine").fit(tf_idf_lookup)

vectorizer_long = TfidfVectorizer(
    analyzer=lambda string, n=5: zip(*[string[i:] for i in range(n)])  # type: ignore
)
tf_idf_lookup_long = vectorizer_long.fit_transform(lookup_long)
nbrs_long = NearestNeighbors(n_neighbors=1, n_jobs=-1, metric="cosine").fit(
    tf_idf_lookup_long
)

fliegel = pd.read_csv("Fliegel_WhitePeople_sentiment.csv")

fliegel["geo_person"] = None
fliegel["lat"] = None
fliegel["lon"] = None
fliegel["geo_factoid"] = None
fliegel["factoid_lat"] = None
fliegel["factoid_lon"] = None

csv_file = csv.reader(open("misc/abbreviations.csv", "r"))
abbr = {}
for row in csv_file:
    k, v = row
    abbr[k] = v

drop_indices = []
for index, row in fliegel.iterrows():
    print(index)
    match = False
    line = row["person"]
    for key, val in abbr.items():
        line = line.replace(key, val)
    for char in [";", ".", "(", ")", '"']:
        line = line.replace(char, " ")
    while "  " in line:
        line = line.replace("  ", " ")

    distances, lookup_indices = nbrs.kneighbors(vectorizer.transform([line]))
    if distances[0][0] < 0.2:
        fliegel.at[index, "geo_person"] = lookup[lookup_indices[0][0]]
        fliegel.at[index, "lat"] = fliegel_gazetteer.at[
            lookup_indices[0][0], "latitude"
        ]
        fliegel.at[index, "lon"] = fliegel_gazetteer.at[
            lookup_indices[0][0], "longitude"
        ]
        match = True

    distances, lookup_indices = nbrs_long.kneighbors(vectorizer_long.transform([line]))
    if distances[0][0] < 0.2:
        fliegel.at[index, "geo_person"] = lookup_long[lookup_indices[0][0]]
        fliegel.at[index, "lat"] = fliegel_gazetteer.at[
            lookup_indices[0][0], "latitude"
        ]
        fliegel.at[index, "lon"] = fliegel_gazetteer.at[
            lookup_indices[0][0], "longitude"
        ]
        match = True

    # factoids
    factoid = str(row["factoid"])
    for key, val in abbr.items():
        factoid = factoid.replace(key, val)
    for char in [";", ".", "(", ")", '"']:
        factoid = factoid.replace(char, " ")
    while "  " in factoid:
        factoid = factoid.replace("  ", " ")

    distances, lookup_indices = nbrs.kneighbors(vectorizer.transform([factoid]))
    if distances[0][0] < 0.2:
        fliegel.at[index, "geo_factoid"] = lookup[lookup_indices[0][0]]
        fliegel.at[index, "factoid_lat"] = fliegel_gazetteer.iloc[lookup_indices[0][0]][
            "latitude"
        ]
        fliegel.at[index, "factoid_lon"] = fliegel_gazetteer.iloc[lookup_indices[0][0]][
            "longitude"
        ]
        match = True

    distances, lookup_indices = nbrs_long.kneighbors(
        vectorizer_long.transform([factoid])
    )
    if distances[0][0] < 0.2:
        fliegel.at[index, "geo_factoid"] = lookup_long[lookup_indices[0][0]]
        fliegel.at[index, "factoid_lat"] = fliegel_gazetteer.iloc[lookup_indices[0][0]][
            "latitude"
        ]
        fliegel.at[index, "factoid_lon"] = fliegel_gazetteer.iloc[lookup_indices[0][0]][
            "longitude"
        ]
        match = True
    if not match:
        drop_indices.append(index)


fliegel = fliegel.drop(drop_indices)


fliegel.to_csv("interim/white_ppl_index_geocoded.csv", index=False)
