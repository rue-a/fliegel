import pandas as pd


admin_lvls = pd.DataFrame()


countries = pd.read_csv("admin_codes/downloads/countries.csv", delimiter="\t")
admin1 = pd.read_csv(
    "admin_codes/downloads/geonames_admin1CodesASCII.csv", delimiter="\t"
)
admin2 = pd.read_csv("admin_codes/downloads/geonames_admin2Codes.csv", delimiter="\t")

lvls0 = []
lvls1 = []
lvls2 = []
for index, row in admin2.iterrows():
    stop = False
    lvl2 = row["name_en"]
    lvl1_code = f"{row['admin_code'].split('.')[0]}.{row['admin_code'].split('.')[1]}"
    lvl1 = admin1.loc[admin1["admin_code"] == lvl1_code]["name_en"]
    lvl0_code = row["admin_code"].split(".")[0]
    lvl0 = countries.loc[countries["code"] == lvl0_code]["country"]
    try:
        lvl1.item()
    except:
        stop = True
    try:
        lvl0.item()
    except:
        stop = True
    if not stop:
        lvls0.append(lvl0.item())
        lvls1.append(lvl1.item())
        lvls2.append(lvl2)

    #  break

admin_lvls["admin_level_2"] = lvls2
admin_lvls["admin_level_1"] = lvls1
admin_lvls["admin_level_0"] = lvls0
admin_lvls.to_csv("admin_codes/admin_levels.csv", index=False)
