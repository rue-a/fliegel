# %%
import xml.etree.ElementTree as etree
import pandas as pd


tree = etree.parse("fliegel_geogNames.xml")
root = tree.getroot()


places = root.findall("place")

geo_names = []
for place in places:
    # each place has exactly one geog name
    if place.find("geogName") != None:
        geogName = place.find("geogName").text
        geogName = geogName.replace("\n", " ")
        while "  " in geogName:
            geogName = geogName.replace("  ", " ")
        geogName = geogName.strip(" ")
        geo_names.append(geogName)

fliegel_geog_df = pd.DataFrame(data=list(set(geo_names)))
fliegel_geog_df = fliegel_geog_df.reset_index()
fliegel_geog_df.columns = ["id", "headline"]


fliegel_geog_df.to_csv("./interim/fliegel_geog_names.csv", index=False)

# %%
