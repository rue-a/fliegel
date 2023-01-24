import pandas as pd
import csv

fliegel = pd.read_csv("./interim/fliegel_geog_names.csv", index_col="id")


# replace abbreviations
reader = csv.reader(open("misc/abbreviations.csv", "r"))
abbr = {}
for row in reader:
    k, v = row

    abbr[k] = v

for index, row in fliegel.iterrows():
    line = row["headline"]
    for key, val in abbr.items():
        line = line.replace(key, val)
    fliegel.at[index, "headline"] = line

# manual things
for index, row in fliegel.iterrows():
    line = row["headline"]
    line = line.replace("Surinam", "Suriname")
    fliegel.at[index, "headline"] = line


# remove trailing stops, double spaces and quotas
# replace ",(" and ", (" with "("
for index, row in fliegel.iterrows():
    line = row["headline"]
    line = line.rstrip(".")
    line = line.replace('"', "")
    line = line.replace(", (", " (")
    line = line.replace(",(", " (")
    while "  " in line:
        line = line.replace("  ", " ")
    fliegel.at[index, "headline"] = line


# resolve into scheme (place_name (synonyms), admin_2, admin_1, admin_0, continent, notes)
fliegel["place_name"] = fliegel["headline"]
fliegel["alternate_names"] = None
fliegel["admin_level_2"] = None
fliegel["admin_level_1"] = None
fliegel["admin_level_0"] = None
fliegel["continent"] = None
fliegel["notes"] = ""


# alternate names in paranthesis
for index, row in fliegel.iterrows():
    alternate_names = []
    line = row["headline"]
    paranthesis_pairs = []
    pair = []
    for i, char in enumerate(line):
        if char == "(":
            pair.append(i)
        if char == ")":
            pair.append(i)
        if len(pair) == 2:
            paranthesis_pairs.append(pair)
            pair = []
    for pair in reversed(paranthesis_pairs):
        replace = line[pair[0] : pair[1] + 1]
        keep = line[pair[0] + 1 : pair[1]]
        keep = keep.split(",")
        keep = [k.strip() for k in keep]
        alternate_names += keep
        line = line.replace(replace, "")
        line = line.replace("  ", " ")

    if alternate_names:
        fliegel.at[index, "alternate_names"] = alternate_names
        fliegel.at[index, "place_name"] = line


continents = ["North America", "South America", "Europe", "Asia", "Australia", "Africa"]
countries = pd.read_csv("admin_codes/downloads/countries.csv", delimiter="\t")
countries = list(countries["country"])
# print(countries)
admin_lvl_names = pd.read_csv("admin_codes/admin_levels.csv")

# repeat multiple times, bcs notes are on random palces
for run_nb in range(5):
    # continents
    for index, row in fliegel.iterrows():
        headline = row["place_name"].split(",")
        if headline[-1].strip() in continents:
            fliegel.at[index, "continent"] = headline[-1].strip()
            headline.pop(-1)
            fliegel.at[index, "place_name"] = ",".join(headline)
    # countries
    for index, row in fliegel.iterrows():
        headline = row["place_name"].split(",")
        if headline[-1].strip() in countries:
            if pd.isna(fliegel.at[index, "admin_level_0"]):
                fliegel.at[index, "admin_level_0"] = headline[-1].strip()
            headline.pop(-1)
            fliegel.at[index, "place_name"] = ",".join(headline)

    # states, counties
    for admin_lvl in ["admin_level_1", "admin_level_2"]:
        for index, row in fliegel.iterrows():
            headline = row["place_name"].split(",")
            if headline[-1].strip() in list(admin_lvl_names[admin_lvl]):
                # if headline[-1].strip() != "Wyoming":
                if pd.isna(fliegel.at[index, admin_lvl]):
                    fliegel.at[index, admin_lvl] = headline[-1].strip()
                headline.pop(-1)
                fliegel.at[index, "place_name"] = ",".join(headline)

    # notes
    for index, row in fliegel.iterrows():
        headline = row["place_name"].split(",")
        if len(headline) > 1:
            if run_nb > 0:
                fliegel.at[index, "notes"] += f" | {headline.pop(-1).strip()}"
            else:
                fliegel.at[index, "notes"] += headline.pop(-1).strip()
            fliegel.at[index, "place_name"] = ",".join(headline)

for index, row in fliegel.iterrows():
    fliegel.at[index, "place_name"] = row["place_name"].strip()

for index, row in fliegel.iterrows():
    place_name = row["place_name"]
    if not place_name:
        place_name = row["admin_level_2"]
    if not place_name:
        place_name = row["admin_level_1"]
    if not place_name:
        place_name = row["admin_level_0"]
    if not place_name:
        place_name = row["continent"]
    fliegel.at[index, "place_name"] = place_name

fliegel = fliegel.drop(["headline"], axis=1)
# fliegel = fliegel.sort_values(["place_name"])
fliegel.to_csv("interim/fliegel_schematized.csv", index=False)
