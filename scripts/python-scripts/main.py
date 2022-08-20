# %%
import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.io as pio
import requests

from visualise import colors_to_colorscale, colorsquare, data2color

# %%

# Load data

df_food = pd.read_csv(
    Path("data", "processed", "fast_food_data_2015.csv",), index_col="borough",
)

df_child = pd.read_csv(
    Path("data", "processed", "child_obesity_data_2015.csv",), index_col="borough",
)

# %%

# Join df's
df = (
    df_child.join(df_food, how="inner",)
    .astype({"rate_per_100,000": float, "outlet_counts": int})
    .dropna(subset="outlet_counts")
)

#%%
p_thresh = np.percentile(df["outlet_counts"], [33, 66])
h_thresh = np.percentile(df["yr6_obesity_prevalence_%"], [33, 66])


# %%

# Download files from URL
url = "https://skgrange.github.io/www/data/london_boroughs.json"
myfile = requests.get(url)
uk_json = json.loads(myfile.content)

#%%

# Find the midpoint of each borough
# Take the average of the longitude and latitude
lons = []
lats = []

for index in range(len(uk_json["features"])):
    longitude = []
    lattitude = []

    for i in range(len(uk_json["features"][index]["geometry"]["coordinates"][0][0])):
        longitude.append(
            uk_json["features"][index]["geometry"]["coordinates"][0][0][i][0]
        )
        lattitude.append(
            uk_json["features"][index]["geometry"]["coordinates"][0][0][i][1]
        )

    lons.append(np.mean(longitude))
    lats.append(np.mean(lattitude))

# Select boroughs
counties = [
    uk_json["features"][k]["properties"]["name"]
    for k in range(len(uk_json["features"]))
]

# borough numbers
tx_ids = [
    uk_json["features"][k]["properties"]["id"] for k in range(len(uk_json["features"]))
]

# %%

# Colours
jstevens = [
    "#e8e8e8",
    "#ace4e4",
    "#5ac8c8",
    "#dfb0d6",
    "#a5add3",
    "#5698b9",
    "#be64ac",
    "#8c62aa",
    "#3b4994",
]

# Extract the data related to each borough
p_ratio = []
h_ratio = []

for bor in counties:
    if bor in ["Hackney", "City of London"]:
        pass
    else:
        p_ratio.append(df.loc[bor, "outlet_counts"])

for bor in counties:
    if bor in ["Hackney", "City of London"]:
        pass
    else:
        h_ratio.append(df.loc[bor, "yr6_obesity_prevalence_%"])

# %%

# Set colour code for each borough
facecolor = data2color(
    p_ratio,
    h_ratio,
    a=p_thresh[0],
    b=p_thresh[1],
    c=h_thresh[0],
    d=h_thresh[1],
    biv_colors=jstevens,
)

# Add markers with text for each borough
text = [
    c
    + "<br>Outlet count: "
    + "{:0.4f}".format(p)
    + "<br>Yr 6 Obesity prevalence %: "
    + "{:0.4f}".format(h)
    for c, p, h in zip(counties, p_ratio, h_ratio)
]

# Set city centre
county_centers = dict(
    type="scatter",
    y=lats,
    x=lons,
    mode="markers",
    text=text,
    marker=dict(size=1, color=facecolor),
    showlegend=False,
    hoverinfo="text",
)

# %%

# Extract boundary of each borough as fill area with boundary
n = len(jstevens)
data = []
fc = np.array(facecolor)

for k in range(9):

    idx_color = np.where(fc == jstevens[k])[0]

    for i in idx_color:

        pts = []

        feature = uk_json["features"][i]

        if feature["geometry"]["type"] == "Polygon":

            pts.extend(feature["geometry"]["coordinates"][0])

            # mark the end of a polygon
            pts.append([None, None])

        elif feature["geometry"]["type"] == "MultiPolygon":

            for polyg in feature["geometry"]["coordinates"]:

                pts.extend(polyg[0])

                # end of polygon
                pts.append([None, None])
        else:
            raise ValueError("geometry type irrelevant for a map")

        X, Y = zip(*pts)

        data.append(
            dict(
                type="scatter",
                x=X,
                y=Y,
                fill="toself",
                fillcolor=jstevens[k],  # facecolor[i],
                hoverinfo="none",
                mode="lines",
                line=dict(width=1, color="rgb(150,150,150)"),
                opacity=0.95,
            )
        )

data.append(county_centers)

# Text for legend
text_x = [
    "LOW outlet_counts",
    "MED outlet_counts",
    "HIGH outlet_counts",
]

text_y = [
    "LOW yr6_obesity_prevalence_%",
    "MED yr6_obesity_prevalence_%",
    "HIGH yr6_obesity_prevalence_%",
]

legend = colorsquare(text_x, text_y, colors_to_colorscale(jstevens))
data.append(legend)
legend_axis = dict(
    showline=False, zeroline=False, showgrid=False, ticks="", showticklabels=False
)

# Configure the plot
layout = dict(
    title="Bivariate Choropleth of London Boroughs: Yr 6 Obesity Prevalence vs Count of Fast Food Outlets 2015",
    font=dict(family="Balto"),
    showlegend=False,
    hovermode="closest",
    xaxis=dict(
        autorange=True,
        range=[-110, -90],
        domain=[0, 1],
        showgrid=False,
        zeroline=False,
        fixedrange=True,
        ticks="",
        showticklabels=False,
    ),
    yaxis=dict(
        autorange=True,
        range=[25, 38],
        domain=[0, 1],
        showgrid=False,
        zeroline=False,
        ticks="",
        showticklabels=False,
        fixedrange=True,
    ),
    xaxis2=dict(
        legend_axis,
        **dict(
            domain=[0.6, 0.75],
            anchor="y2",
            side="top",
            title="P_33, P_66 are percentiles",
            titlefont=dict(size=11),
        ),
    ),
    yaxis2=dict(legend_axis, **dict(domain=[0.735, 0.885], anchor="x2"),),
    width=1100,
    height=850,
    dragmode="select",
)
# %%

# Plot Figure
fig = dict(data=data, layout=layout,)
pio.write_html(
    fig, file="Texas-bivariates.html", auto_open=True,
)

# %%
