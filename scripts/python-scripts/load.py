# %%
from operator import index
from pathlib import Path

import pandas as pd

# %%
# 2017 Childhood data loading
df = (
    pd.read_excel(
        Path("portfolio", "project", "data", "raw", "child_obesity_data_2017.xlsx"),
        usecols=["Unnamed: 23", "Unnamed: 1"],
        skiprows=3,
    )
    .rename(
        {"Unnamed: 23": "yr6_obesity_prevalence_%", "Unnamed: 1": "borough"},
        axis="columns",
    )
    .set_index("borough")
).dropna(axis=0, how="all",)

# Save df to processed
df.to_csv(
    Path("portfolio", "project", "data", "processed", "child_obesity_data_2017.csv")
)


# %%
# 2015 Childhood data loading
df = (
    pd.read_excel(
        Path("portfolio", "project", "data", "raw", "child-obesity-data-2015.xlsx"),
        usecols=["Unnamed: 23", "Unnamed: 1"],
        skiprows=3,
    )
    .rename(
        {"Unnamed: 23": "yr6_obesity_prevalence_%", "Unnamed: 1": "borough"},
        axis="columns",
    )
    .set_index("borough")
).dropna(axis=0, how="all",)

# Save df to processed
df.to_csv(
    Path("portfolio", "project", "data", "processed", "child_obesity_data_2015.csv")
)


# %%
# 2017 fast food data loading
df = (
    pd.read_excel(
        Path("portfolio", "project", "data", "raw", "fast_food_data_2017.xlsx"),
        sheet_name="Local Authority Data",
        skiprows=[0, 1, 2],
        usecols=[
            "PHE Centre",
            "LA name",
            "Count of outlets",
            "Rate per 100,000 population",
        ],
    )
    .rename(
        {
            "PHE Centre": "phe_centre",
            "LA name": "borough",
            "Count of outlets": "outlet_counts",
            "Rate per 100,000 population": "rate_per_100,000",
        },
        axis="columns",
    )
    .dropna(how="all", axis=0)
)

# Subset on London boroughs
df = df[df["phe_centre"] == "London"].set_index("borough").drop("phe_centre", axis=1)

# Save df to processed
df.to_csv(Path("portfolio", "project", "data", "processed", "fast_food_data_2017.csv"))


# %%
# 2015 fast food data
df = (
    pd.read_excel(
        Path("portfolio", "project", "data", "raw", "fast-food-data-2015.xlsx"),
        sheet_name="Local Authority Data",
        skiprows=[0, 1, 2],
        usecols=[
            "PHE Centre",
            "LA name",
            "Count of outlets",
            "Rate per 100,000 population",
        ],
    )
    .rename(
        {
            "PHE Centre": "phe_centre",
            "LA name": "borough",
            "Count of outlets": "outlet_counts",
            "Rate per 100,000 population": "rate_per_100,000",
        },
        axis="columns",
    )
    .dropna(how="all", axis=0)
)

# Subset on London boroughs
df = df[df["phe_centre"] == "London"].set_index("borough").drop("phe_centre", axis=1)

# %%
# Save df to processed
df.to_csv(Path("portfolio", "project", "data", "processed", "fast_food_data_2015.csv"))

# %%
