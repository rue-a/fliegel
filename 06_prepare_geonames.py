import pandas as pd


columns = [
    "geonameid",
    "name",
    "asciiname",
    "alternatenames",
    "latitude",
    "longitude",
    "feature class",
    "feature code",
    "country code",
    "cc2",
    "admin1 code",
    "admin2 code",
    "admin3 code",
    "admin4 code",
    "population",
    "elevation",
    "dem",
    "timezone",
    "modification date",
]
dtypes = {"admin1 code": object, "admin2 code": object}

austria = pd.read_csv(
    "geonames/AT.txt", delimiter="\t", low_memory=False, names=columns, dtype=dtypes
)
barbados = pd.read_csv(
    "geonames/BB.txt", delimiter="\t", low_memory=False, names=columns
)
canada = pd.read_csv(
    "geonames/CA.txt",
    delimiter="\t",
    low_memory=False,
    names=columns,
    dtype=dtypes,
)
switzerland = pd.read_csv(
    "geonames/CH.txt", delimiter="\t", low_memory=False, names=columns, dtype=dtypes
)
germany = pd.read_csv(
    "geonames/DE.txt", delimiter="\t", low_memory=False, names=columns, dtype=dtypes
)
denmark = pd.read_csv(
    "geonames/DK.txt", delimiter="\t", low_memory=False, names=columns, dtype=dtypes
)
spain = pd.read_csv(
    "geonames/ES.txt", delimiter="\t", low_memory=False, names=columns, dtype=dtypes
)
france = pd.read_csv(
    "geonames/FR.txt", delimiter="\t", low_memory=False, names=columns, dtype=dtypes
)
greenland = pd.read_csv(
    "geonames/GL.txt", delimiter="\t", low_memory=False, names=columns
)
guyana = pd.read_csv("geonames/GY.txt", delimiter="\t", low_memory=False, names=columns)
guinea = pd.read_csv("geonames/GN.txt", delimiter="\t", low_memory=False, names=columns)
ireland = pd.read_csv(
    "geonames/IE.txt", delimiter="\t", low_memory=False, names=columns, dtype=dtypes
)
jamaica = pd.read_csv(
    "geonames/JM.txt", delimiter="\t", low_memory=False, names=columns, dtype=dtypes
)
lebanon = pd.read_csv(
    "geonames/LB.txt", delimiter="\t", low_memory=False, names=columns, dtype=dtypes
)
mexico = pd.read_csv(
    "geonames/MX.txt", delimiter="\t", low_memory=False, names=columns, dtype=dtypes
)
russia = pd.read_csv(
    "geonames/RU.txt", delimiter="\t", low_memory=False, names=columns, dtype=dtypes
)
south_africa = pd.read_csv(
    "geonames/ZA.txt", delimiter="\t", low_memory=False, names=columns
)
sweden = pd.read_csv(
    "geonames/SE.txt", delimiter="\t", low_memory=False, names=columns, dtype=dtypes
)
suriname = pd.read_csv(
    "geonames/SR.txt", delimiter="\t", low_memory=False, names=columns, dtype=dtypes
)
united_states = pd.read_csv(
    "geonames/US.txt", delimiter="\t", low_memory=False, names=columns
)

geonames = pd.concat(
    [
        austria,
        barbados,
        canada,
        denmark,
        france,
        germany,
        guyana,
        greenland,
        guinea,
        ireland,
        jamaica,
        lebanon,
        mexico,
        russia,
        spain,
        south_africa,
        sweden,
        switzerland,
        suriname,
        united_states,
    ]
)
geonames.drop("geonameid", inplace=True, axis=1)
geonames.drop("name", inplace=True, axis=1)
geonames.drop("feature code", inplace=True, axis=1)
geonames.drop("cc2", inplace=True, axis=1)
geonames.drop("admin3 code", inplace=True, axis=1)
geonames.drop("admin4 code", inplace=True, axis=1)
# geonames.drop("population", inplace=True, axis=1)
geonames.drop("elevation", inplace=True, axis=1)
geonames.drop("dem", inplace=True, axis=1)
geonames.drop("timezone", inplace=True, axis=1)
geonames.drop("modification date", inplace=True, axis=1)


# print(set(list(fliegel["admin_level_0"])))
# {'Guinea', 'Canada', 'France', 'Russia', 'Suriname', 'Sweden', 'Switzerland', 'Spain', 'Austria', 'Greenland', 'Mexico', 'Jamaica', 'Georgia', 'Lebanon', 'Ireland', 'Denmark', 'Germany'}
# geonames = pd.read_csv("")
geonames = geonames[geonames["asciiname"].notna()]
geonames.to_csv("geonames/geonames_prepared.csv", index=False)
