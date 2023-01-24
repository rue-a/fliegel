# %%
import pandas as pd

fliegel = pd.read_csv("interim/white_ppl_index_geocoded.csv").drop(columns=["index"])


drop_indices_person = []
drop_indices_factoid = []
drop_indices_person_and_factoid = []
for index, row in fliegel.iterrows():
    if pd.isna(row["geo_person"]):
        drop_indices_person.append(index)
    if pd.isna(row["geo_factoid"]):
        drop_indices_factoid.append(index)
    if pd.isna(row["geo_factoid"]) or pd.isna(row["geo_person"]):
        drop_indices_person_and_factoid.append(index)
    if row["geo_factoid"] == "Augusta" or row["geo_person"] == "Augusta":
        drop_indices_person_and_factoid.append(index)
    if row["geo_factoid"] == "Augusta":
        drop_indices_factoid.append(index)
    if row["geo_person"] == "Augusta":
        drop_indices_person.append(index)

fliegel_person = fliegel.drop(drop_indices_person)
fliegel_factoid = fliegel.drop(drop_indices_factoid)
fliegel_person_and_factoid = fliegel.drop(drop_indices_person_and_factoid)

fliegel_person.to_csv("fliegel_geoperson.csv", index=False)
fliegel_factoid.to_csv("fliegel_geofactoid.csv", index=False)
fliegel_person_and_factoid.to_csv("fliegel_geoperson_and_geofactoid.csv", index=False)

from pprint import pprint

locs = list(fliegel_person_and_factoid["geo_person"]) + list(
    fliegel_person_and_factoid["geo_factoid"]
)

# some analysis
freq = {}
for loc in list(set(locs)):
    freq[loc] = 0
for loc in locs:
    freq[loc] += 1
freq = sorted(freq.items(), key=lambda x: x[1])
pprint(freq)
