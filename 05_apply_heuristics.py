import pandas as pd

admin_lvl_names = pd.read_csv("admin_codes/admin_levels.csv")
countries = pd.read_csv("admin_codes/downloads/countries.csv", delimiter="\t")
countries = list(countries["country"])
fliegel = pd.read_csv("interim/fliegel_condensed.csv")
fliegel["feature_type"] = None

hydrographic_terms = ["river", "creek", "falls", "ocean", "coast", "bay", "gulf"]
admin_terms = []
area_terms = ["area", "territory"]
populated_terms = []
road_railroad_terms = []
spot_terms = ["point"]
hypsographic_terms = ["valley", "hill", "mountains", "mountain", "cape"]
vegetation_terms = []
undersea_terms = []

feat_class_dict = {
    "A": admin_terms,
    "H": hydrographic_terms,
    "L": area_terms,
    "P": populated_terms,
    "R": road_railroad_terms,
    "S": spot_terms,
    "T": hypsographic_terms,
    "U": undersea_terms,
    "V": vegetation_terms,
}

for index, row in fliegel.iterrows():
    for feat_type, indicators in feat_class_dict.items():
        for indicator in indicators:
            if (
                indicator in row["place_name"]
                or indicator.capitalize() in row["place_name"]
            ):
                fliegel.at[index, "feature_type"] = feat_type
    # if (
    #     row["place_name"] == row["admin_level_2"]
    #     or row["place_name"] == row["admin_level_1"]
    #     or row["place_name"] == row["admin_level_0"]
    #     or row["place_name"] == row["continent"]
    # ):
    #     fliegel.at[index, "feature_type"] = "A"

    if not pd.isna(row["notes"]):
        if " in " in row["notes"]:
            place = row["notes"].split(" in ")[-1].split(" ")[0]
            if place in countries:
                fliegel.at[index, "admin_level_0"] = place
            if place in list(admin_lvl_names["admin_level_1"]):
                fliegel.at[index, "admin_level_1"] = place
            if place in list(admin_lvl_names["admin_level_2"]):
                fliegel.at[index, "admin_level_2"] = place
            try:
                place = (
                    row["notes"].split(" in ")[-1].split(" ")[0]
                    + " "
                    + row["notes"].split(" in ")[-1].split(" ")[1]
                )
                if place in countries:
                    fliegel.at[index, "admin_level_0"] = place
                if place in list(admin_lvl_names["admin_level_1"]):
                    fliegel.at[index, "admin_level_1"] = place
                if place in list(admin_lvl_names["admin_level_2"]):
                    fliegel.at[index, "admin_level_2"] = place
            except:
                pass
    if " in " in row["place_name"]:
        place = row["place_name"].split(" in ")[-1].split(" ")[0]
        if place in countries:
            fliegel.at[index, "admin_level_0"] = place
        if place in list(admin_lvl_names["admin_level_1"]):
            fliegel.at[index, "admin_level_1"] = place
        if place in list(admin_lvl_names["admin_level_2"]):
            fliegel.at[index, "admin_level_2"] = place
        try:
            place = (
                row["place_name"].split(" in ")[-1].split(" ")[0]
                + " "
                + row["place_name"].split(" in ")[-1].split(" ")[1]
            )
            if place in countries:
                fliegel.at[index, "admin_level_0"] = place
            if place in list(admin_lvl_names["admin_level_1"]):
                fliegel.at[index, "admin_level_1"] = place
            if place in list(admin_lvl_names["admin_level_2"]):
                fliegel.at[index, "admin_level_2"] = place
        except:
            pass


fliegel.to_csv("interim/fliegel_typed.csv", index=False)
