import pandas as pd


fliegel = pd.read_csv("interim/fliegel_geocoded.csv")
fliegel_admin_names = pd.read_csv("interim/fliegel_condensed.csv")
fliegel["admin_level_2"] = fliegel_admin_names["admin_level_2"]
fliegel["admin_level_1"] = fliegel_admin_names["admin_level_1"]
fliegel["admin_level_0"] = fliegel_admin_names["admin_level_0"]
fliegel = fliegel.drop(fliegel[pd.isna(fliegel["latitude"])].index)

fliegel = fliegel.drop(fliegel[fliegel["place_name"] == "Moravia"].index)

fliegel.to_csv("fliegel_gazetteer.csv", index=False)
