# %%
import pandas as pd
import csv
import math
from functools import reduce



fliegel = pd.read_csv("interim/fliegel_schematized.csv")
fliegel = fliegel.sort_values(["place_name"])
# fliegel_condensed = pd.DataFrame(columns=fliegel.columns)

# define how to aggregate various fields
# agg_functions = {'employee': 'first', 'sales': 'sum', 'returns': 'sum'}

# create new DataFrame by combining rows with same id values


# fliegel = fliegel.groupby(fliegel["place_name"], as_index=False).apply(alt_names)
# fliegel = fliegel.groupby(fliegel["place_name"], group_keys=False).apply(
#     lambda df: df["altername_names"].sum()
# )
def add_lists(a, b):
    if pd.isna(a) and pd.isna(b):
        return None
    if pd.isna(a):
        return b
    if pd.isna(b):
        return a
    return a + b


def add_admins(a, b):
    if pd.isna(a) and pd.isna(b):
        return None
    if pd.isna(a):
        return b
    if pd.isna(b):
        return a
    if b not in a:
          
    return a + " & " + b  else a

def add_strings(a, b):
    if pd.isna(a) and pd.isna(b):
        return None
    if pd.isna(a):
        return b
    if pd.isna(b):
        return a
    return a + " & " + b if b not in a else a

def condense_lists(series):
    return reduce(add_lists, series)


def condense_admin(series):
    return reduce(add_admins, series)

def condense_strings(series):
    return reduce(add_strings, series)



fliegel = fliegel.groupby(fliegel["place_name"], as_index=False).agg(
    {
        "alternate_names": [condense_lists],
        "admin_level_2": [condense_admin],
        "admin_level_1": [condense_admin],
        "admin_level_0": [condense_admin],
        "continent": [condense_admin],
        "notes": [condense_strings],
    }
)
# print(pd.DataFrame(groups).iloc[1265][1])

# print(len(groups))
fliegel.to_csv("interim/fliegel_condensed.csv", index=False)

# %%
