# %%
import pandas as pd

fliegel = pd.read_csv("interim/fliegel_schematized.csv")
fliegel = fliegel.sort_values(
    ["place_name"],
    ignore_index=True,
)
# print(fliegel)
fliegel["alternate_names"] = fliegel["alternate_names"].fillna("[]")
for col in fliegel.columns[2:]:
    fliegel[col] = fliegel[col].fillna("")
# print(fliegel)

remove_indices = []
for index in reversed(fliegel.index):
    if index == 1:
        break

    current_row = fliegel.iloc[index]  # type: ignore
    next_row = fliegel.iloc[index - 1]  # type: ignore
    if current_row["place_name"] == next_row["place_name"]:
        countries_equal = current_row["admin_level_0"] == next_row["admin_level_0"]
        states_equal = current_row["admin_level_1"] == next_row["admin_level_1"]
        counties_equal = current_row["admin_level_2"] == next_row["admin_level_2"]
        if (
            (countries_equal and states_equal and counties_equal)
            or (
                countries_equal
                and states_equal
                and current_row["admin_level_2"]
                and not next_row["admin_level_2"]
            )
            or (
                countries_equal
                and counties_equal
                and current_row["admin_level_1"]
                and not next_row["admin_level_1"]
            )
            or (
                states_equal
                and counties_equal
                and current_row["admin_level_0"]
                and not next_row["admin_level_0"]
            )
        ):
            try:
                current_row["alternate_names"] = eval(current_row["alternate_names"])
            except:
                pass
            try:
                next_row["alternate_names"] = eval(next_row["alternate_names"])
            except:
                pass
            if current_row["alternate_names"]:
                if not next_row["alternate_names"]:
                    fliegel.at[index - 1, "alternate_names"] = current_row[  # type: ignore
                        "alternate_names"
                    ]
                else:
                    fliegel.at[index - 1, "alternate_names"] = list(  # type: ignore
                        set(
                            next_row["alternate_names"] + current_row["alternate_names"]
                        )
                    )
            if current_row["notes"]:
                if not next_row["notes"]:
                    fliegel.at[index - 1, "notes"] = current_row["notes"]  # type: ignore
                else:
                    fliegel.at[index - 1, "notes"] = (  # type: ignore
                        next_row["notes"] + " & " + current_row["notes"]
                    )
                    # print(next_row["notes"] + " & " + current_row["notes"])
            fliegel.at[index - 1, "admin_level_0"] = current_row["admin_level_0"]
            fliegel.at[index - 1, "admin_level_1"] = current_row["admin_level_1"]
            fliegel.at[index - 1, "admin_level_2"] = current_row["admin_level_2"]

            remove_indices.append(index)
        if (
            (countries_equal and states_equal and counties_equal)
            or (
                countries_equal
                and states_equal
                and not current_row["admin_level_2"]
                and next_row["admin_level_2"]
            )
            or (
                countries_equal
                and counties_equal
                and not current_row["admin_level_1"]
                and next_row["admin_level_1"]
            )
            or (
                states_equal
                and counties_equal
                and not current_row["admin_level_0"]
                and next_row["admin_level_0"]
            )
        ):
            try:
                current_row["alternate_names"] = eval(current_row["alternate_names"])
            except:
                pass
            try:
                next_row["alternate_names"] = eval(next_row["alternate_names"])
            except:
                pass
            if current_row["alternate_names"]:
                if not next_row["alternate_names"]:
                    fliegel.at[index - 1, "alternate_names"] = current_row[  # type: ignore
                        "alternate_names"
                    ]
                else:
                    fliegel.at[index - 1, "alternate_names"] = list(  # type: ignore
                        set(
                            next_row["alternate_names"] + current_row["alternate_names"]
                        )
                    )
            if current_row["notes"]:
                if not next_row["notes"]:
                    fliegel.at[index - 1, "notes"] = current_row["notes"]  # type: ignore
                else:
                    fliegel.at[index - 1, "notes"] = (  # type: ignore
                        next_row["notes"] + " & " + current_row["notes"]
                    )
                    # print(next_row["notes"] + " & " + current_row["notes"])

            remove_indices.append(index)

    # if index == 1746:
    #     break

# fliegel.to_csv("interim/fliegel_condensed.csv", index=False)
# for ind in remove_indices:
#     print(ind)
fliegel.drop(remove_indices, inplace=True)
fliegel.to_csv("interim/fliegel_condensed.csv", index=False)
