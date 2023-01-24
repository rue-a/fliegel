import pandas as pd
import geopandas as gpd
from shapely.wkt import loads
from functools import reduce

fliegel = pd.read_csv("fliegel_geofactoid.csv")
# %%

# ony keep years
drop = []
for index, row in fliegel.iterrows():
    if pd.isna(row["year"]) or row["year"] == "no date":
        drop.append(index)

    else:
        year = str(row["year"])
        if "-" in row["year"]:
            year = row["year"].split("-")[0]
        fliegel.at[index, "year"] = [year]
        fliegel.at[index, "factoid_lat"] = [str(row["factoid_lat"])]
        fliegel.at[index, "factoid_lon"] = [str(row["factoid_lon"])]
fliegel = fliegel.drop(drop)


# rename zeisberger rows
rename = {
    "Zeisberger, David, Moravian missionary: Conferences.": "Zeisberger, David",
    "Zeisberger, David, Moravian missionary: Journeys.": "Zeisberger, David",
    "Zeisberger, David, Moravian missionary: Linguistic work.": "Zeisberger, David",
    "Zeisberger, David, Moravian missionary: Pastor and Preacher.": "Zeisberger, David",
    "Zeisberger, David, Moravian missionary: Personal Life.": "Zeisberger, David",
    "Zeisberger, David, Moravian missionary: Planning and disposing.": "Zeisberger, David",
    "Zeisberger, David, Moravian missionary: Relations with Indians.": "Zeisberger, David",
    "Zeisberger, David, Moravian missionary: Visits.": "Zeisberger, David",
    "Zeisberger, David, Moravian missionary; Involved in public affairs.": "Zeisberger, David",
}
for index, row in fliegel.iterrows():
    if row["person"] in rename.keys():
        fliegel.at[index, "person"] = rename[row["person"]]


def add_lists(a, b):
    return a + b


def condense_year(series):
    return reduce(add_lists, series)


def condense_lat(series):
    return reduce(add_lists, series)


def condense_lon(series):
    return reduce(add_lists, series)


fliegel = fliegel.groupby(fliegel["person"]).agg(
    {
        "year": [condense_year],
        "factoid_lon": [condense_lat],
        "factoid_lat": [condense_lon],
    }
)

fliegel = pd.concat([fliegel])
fliegel = fliegel.rename(
    columns={
        "condense_year": "years",
        "condense_lat": "factoid_lons",
        "condense_lon": "factoid_lats",
    }
)

fliegel.columns = fliegel.columns.droplevel(0)
fliegel = fliegel.reset_index(level=0)

drop = []
fliegel["points"] = None
fliegel["linestring"] = None
for index, row in fliegel.iterrows():
    years, lats, lons = (
        (row["years"]),
        (row["factoid_lons"]),
        (row["factoid_lats"]),
    )
    if len(years) > 1:
        inds = range(0, len(years))

        d = dict(zip(inds, [[years[k], lats[k], lons[k]] for k in range(len(years))]))
        d = sorted(d.items(), key=lambda x: x[1])
        # print(d)

        l = [l[1] for l in d]
        points = []
        linestring = "LINESTRING ("
        for triple in l:
            year, lon, lat = triple
            point = f"{year}, POINT ({lon} {lat})"
            points.append(point)

            linestring += f"{lon} {lat}, "
        linestring = linestring.strip().strip(",")
        linestring += ")"

        fliegel.at[index, "points"] = points
        fliegel.at[index, "linestring"] = linestring

    else:
        drop.append(index)


fliegel = fliegel.drop(drop)
fliegel = fliegel.drop(columns=["years", "factoid_lats", "factoid_lons"])

fliegel_lines = fliegel

fliegel_lines["geometry"] = fliegel_lines["linestring"].apply(loads)
fliegel_lines = gpd.GeoDataFrame(fliegel_lines, geometry="geometry", crs="EPSG:4326")
fliegel_lines.drop(columns=["points"]).to_file(
    "geojsons/person_travels.geojson", driver="GeoJSON"
)


for item, row in fliegel.iterrows():
    years = []
    geoms = []
    for point in row["points"]:
        year, geom = point.split(", ", 1)
        years.append(year)
        geoms.append(loads(geom))
    gdf = gpd.GeoDataFrame(geometry=geoms, crs="EPSG:4326")
    gdf["year"] = years
    # gdf["geometry"] = geoms
    filename = (
        row["person"]
        .replace(" ", "")
        .replace("?", "")
        .replace("[", "")
        .replace("]", "")
        .replace("(", "")
        .replace(")", "")
        .replace('"', "")
        .replace(",", "_")
        .replace(";", "_")
        .replace(":", "_")
        .strip(".")
    )
    gdf.to_file(f"geojsons/single_person_travels/{filename}.geojson", driver="GeoJSON")


# fliegel = fliegel.drop(columns=["points"])
