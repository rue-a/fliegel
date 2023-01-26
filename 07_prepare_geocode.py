import pandas as pd


countries = pd.read_csv(
    "admin_codes/downloads/countries.csv", delimiter="\t", low_memory=False
)
admin_1 = pd.read_csv(
    "admin_codes/downloads/geonames_admin1CodesASCII.csv",
    delimiter="\t",
    low_memory=False,
)
admin_2 = pd.read_csv(
    "admin_codes/downloads/geonames_admin2Codes.csv",
    delimiter="\t",
    low_memory=False,
)
fliegel = pd.read_csv("interim/fliegel_typed.csv")
fliegel["ambigous_county"] = None


for index, row in fliegel.iterrows():
    if not pd.isna(row["admin_level_0"]):
        code = countries.loc[countries["country"] == row["admin_level_0"]][
            "code"
        ].item()
        fliegel.at[index, "admin_level_0"] = code
    if not pd.isna(row["admin_level_1"]):
        code = (
            admin_1.loc[admin_1["name_en"] == row["admin_level_1"]]["admin_code"]
            .item()
            .split(".")[-1]
        )
        fliegel.at[index, "admin_level_1"] = code
    if not pd.isna(row["admin_level_2"]):
        codes = admin_2.loc[admin_2["name_en"] == row["admin_level_2"]]["admin_code"]
        if not len(codes) > 1:
            country, state, county = codes.item().split(".")
            if state == row["admin_level_1"]:
                fliegel.at[index, "admin_level_2"] = codes.item().split(".")[-1]
            else:
                fliegel.at[index, "ambigous_county"] = row["admin_level_2"]
                fliegel.at[index, "admin_level_2"] = None
        else:
            print(row["admin_level_2"])
            print(codes)
            code = None
            for item in list(codes):
                country, state, county = item.split(".")
                if state == row["admin_level_1"]:
                    code = item
            if code:
                fliegel.at[index, "admin_level_2"] = code.split(".")[-1]
            else:
                fliegel.at[index, "ambigous_county"] = row["admin_level_2"]
                fliegel.at[index, "admin_level_2"] = None


fliegel.to_csv("interim/fliegel_prepared.csv", index=False)
