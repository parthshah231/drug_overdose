from typing import List

import plotly
import contextily
import mapclassify

import pandas as pd
import geopandas as gpd
import geoplot as gplot
import geoplot.crs as gcrs
import matplotlib.pyplot as plt
import seaborn as sns

from pysal.explore import esda
from pysal.lib import weights

from constants import DATA

if __name__ == "__main__":
    df = pd.read_csv(
        DATA / "CDC Injury Center Drug Overdose Deaths.csv", encoding="ISO-8859-1"
    )

    # print(df.info())

    # sub_df = df.rename(
    #     columns={
    #         "2019 Age-adjusted Rate (per 100,000 population)": "2019",
    #         "2018 Age-adjusted Rate (per 100,000 population)": "2018",
    #         "2017 Age-adjusted Rate (per 100,000 population)": "2017",
    #         "2016 Age-adjusted Rate (per 100,000 population)": "2016",
    #         "2015 Age-adjusted Rate (per 100,000 population)": "2015",
    #         "2014 Age-adjusted Rate (per 100,000 population)": "2014",
    #         "2013 Age-adjusted Rate (per 100,000 population)": "2013",
    #     }
    # )

    # pd.set_option("display.max_columns", None)
    # pd.set_option("display.max_rows", None)

    # sub_df = sub_df[
    #     [
    #         "State",
    #         "2019",
    #         "2018",
    #         "2017",
    #         "2016",
    #         "2015",
    #         "2014",
    #         "2013",
    #     ]
    # ]

    # This says we have some missing values
    # print(df.isna().values.any())
    # Let's confirm where they are
    # print(df.isnull().sum())
    # Since, it's a small dataset of 50 rows, we can look their position
    # Looks like if we drop them we will be dropping District Of Columbia
    # at this state we can either fill it with mean, median, mode or
    # interpolate it.. or just drop it! Let's just drop it for now.
    # sub_df = sub_df.dropna()
    # print(df.shape)

    # sub_df = sub_df.set_index("State")

    # If I plot before this it is taking columns as y axis [years]
    # and we want the other way around.. so transpose
    # transposed_df = sub_df.T
    # print(df.head())
    # print(transposed_df.head())

    # Also, it's showing 2019..2013, let's sort it
    # transposed_df = transposed_df.sort_index()

    # Enlarge the image so that the legend fits!
    # plt.figure(figsize=(15, 15))
    # sns.lineplot(data=transposed_df)
    # plt.show()
    # We see an upward trend from 2013..2019 for almost
    # every state.

    # fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20, 10), sharex=True)
    # sns.barplot(
    #     y=df["2013 Number of Deaths"],
    #     x=df["State Abbreviation"],
    #     data=df,
    #     ax=ax[0],
    # )
    # ax[0].set_title("2013")
    # ax[0].set_ylim(0, 6000)

    # sns.barplot(
    #     y=df["2019 Number of Deaths"],
    #     x=df["State Abbreviation"],
    #     data=df,
    #     ax=ax[1],
    # )
    # ax[1].set_title("2019")
    # plt.show()

    # fig, ax = plt.subplots(figsize=(20, 10))
    # sns.heatmap(sub_df.corr(), annot=True, ax=ax)
    # ax.tick_params(axis="x", rotation=45)
    # plt.show()
    # Definitely, there is a correlation between the years

    # Let's plot choropleth map
    # Choroploth map: https://en.wikipedia.org/wiki/Choropleth_map
    # They are used to represent statistical variables associated with
    # a specific geographical area. The choropleth map provides an
    # easy way to visualize how a measurement varies across a geographic
    # area or it shows the level of variability within a region.

    us = gpd.read_file(gplot.datasets.get_path("contiguous_usa"))
    merged_df = us.set_index("state").join(df.set_index("State"))

    # var = "2013 Number of Deaths"
    # fig, ax = plt.subplots(figsize=(12, 8))
    # ax.axis("off")

    # ax.set_title(
    #     "2013 Number of Deaths", fontdict={"fontsize": "15", "fontweight": "3"}
    # )

    # merged_df.plot(
    #     column=var,
    #     cmap="YlOrRd",
    #     linewidth=0.8,
    #     ax=ax,
    #     edgecolor="0.8",
    #     legend=True,
    # )
    # plt.show()

    # var = "2019 Number of Deaths"
    # fig, ax = plt.subplots(figsize=(12, 8))
    # ax.axis("off")

    # ax.set_title(
    #     "2019 Number of Deaths", fontdict={"fontsize": "15", "fontweight": "3"}
    # )

    # merged_df.plot(
    #     column=var,
    #     cmap="YlOrRd",
    #     linewidth=0.8,
    #     ax=ax,
    #     edgecolor="0.8",
    #     legend=True,
    # )
    # plt.show()

    # It is visually hard to see the difference between the two maps, unless
    # we look at the legend. Let's try to plot the difference between the two
    # maps.

    # merged_df["diff"] = (
    #     merged_df["2019 Number of Deaths"] - merged_df["2013 Number of Deaths"]
    # )

    # var = "diff"
    # fig, ax = plt.subplots(figsize=(12, 8))
    # ax.axis("off")

    # ax.set_title(
    #     "2019 Number of Deaths - 2013 Number of Deaths",
    #     fontdict={"fontsize": "15", "fontweight": "3"},
    # )

    # merged_df.plot(
    #     column=var,
    #     cmap="YlOrRd",
    #     linewidth=0.8,
    #     ax=ax,
    #     edgecolor="0.8",
    #     legend=True,
    # )
    # plt.show()

    # We can see that the difference is not that much, but we can see that
    # the states with the highest difference are California, Texas, Florida,
    # New York, Pennsylvania, Ohio, Illinois, Michigan, Georgia, and North
    # Carolina. These are the states with the highest population in the US.
    # So, it makes sense that the number of deaths is higher in these states.

    # We will use pysal to plot pooled classificaiton map

    # years = [
    #     "2019 Age-adjusted Rate (per 100,000 population)",
    #     "2018 Age-adjusted Rate (per 100,000 population)",
    #     "2014 Age-adjusted Rate (per 100,000 population)",
    #     "2013 Age-adjusted Rate (per 100,000 population)",
    # ]

    # pooled = mapclassify.Pooled(merged_df[years], classifier="Quantiles", k=8)

    # f, axs = plt.subplots(2, 2, figsize=(12, 12))
    # axs = axs.flatten()
    # for i, y in enumerate(years):
    #     merged_df.plot(
    #         y,
    #         scheme="UserDefined",
    #         cmap="YlOrRd",
    #         edgecolor="0.8",
    #         classification_kwds={"bins": pooled.global_classifier.bins},
    #         legend=True,
    #         legend_kwds={"loc": "lower left", "framealpha": 0.3},
    #         ax=axs[i],
    #     )
    #     axs[i].set_axis_off()
    #     axs[i].set_title(y)
    # plt.tight_layout()
    # plt.show()

    # We can cleary see the epidemic spreading from 2013 to 2019. The pooled
    # classification map is a good way to visualize the spread of the epidemic
    # over the years. By keeping the scale constant we can see the change in
    # the color of the states. The darker the color, the higher the number of
    # deaths. We can see that the epidemic is spreading from the west coast to
    # the east coast with the neighboring states starting to have similar
    # colors, is it because of the drug trafficking?

    # The data exihibits significant spatial autocorrelation meaning the states
    # with low number of deaths are surrounded by states with low number of
    # deaths and the states with high number of deaths are surrounded by states
    # with high number of deaths. We can use Moran's I to test for spatial
    # autocorrelation.

    # w = weights.distance.KNN.from_dataframe(merged_df, k=8)
    w = weights.Queen.from_dataframe(merged_df)
    w.transform = "R"

    # Calculate Spatial Lag
    # Spatial lag is the weighted average of the values of a variable among
    # the neighbors of a given unit. The spatial lag of a variable y is
    # defined as: y_lag = w * y
    merged_df["w_2013"] = weights.spatial_lag.lag_spatial(
        w, merged_df["2013 Age-adjusted Rate (per 100,000 population)"]
    )
    merged_df["w_2019"] = weights.spatial_lag.lag_spatial(
        w, merged_df["2019 Age-adjusted Rate (per 100,000 population)"]
    )

    # Standardize the variables
    merged_df["2013 Age-adjusted Rate (per 100,000 population)_std"] = (
        merged_df["2013 Age-adjusted Rate (per 100,000 population)"]
        - merged_df["2013 Age-adjusted Rate (per 100,000 population)"].mean()
    ) / merged_df["2013 Age-adjusted Rate (per 100,000 population)"].std()

    merged_df["2019 Age-adjusted Rate (per 100,000 population)_std"] = (
        merged_df["2019 Age-adjusted Rate (per 100,000 population)"]
        - merged_df["2019 Age-adjusted Rate (per 100,000 population)"].mean()
    ) / merged_df["2019 Age-adjusted Rate (per 100,000 population)"].std()

    # Plot Spatial Lag
    # fig, ax = plt.subplots(figsize=(12, 10))
    # merged_df.plot(
    #     column="w_2019",
    #     cmap="YlOrRd",
    #     linewidth=0.8,
    #     ax=ax,
    #     edgecolor="0.8",
    #     legend=True,
    # )
    # ax.set_axis_off()
    # ax.set_title(
    #     "Spatial Lag of 2019 Age-adjusted Rate (per 100,000 population)_std",
    #     fontdict={"fontsize": "15", "fontweight": "3"},
    # )
    # plt.show()

    # From the spatial lag plot we can see that the states with high number of
    # deaths are surrounded by states with high number of deaths and the states
    # with low number of deaths are surrounded by states with low number of
    # deaths. This is a clear indication of spatial autocorrelation.

    # sns.regplot(
    #     x="2019 Age-adjusted Rate (per 100,000 population)_std",
    #     y="w_2019",
    #     data=merged_df,
    #     scatter_kws={"s": 10},
    #     line_kws={"color": "red"},
    # )
    # plt.show()

    lisa = esda.moran.Moran_Local(
        merged_df["2019 Age-adjusted Rate (per 100,000 population)_std"], w
    )

    # ax = sns.kdeplot(
    #     list(lisa.Is),
    # )
    # ax.set_xlabel("Local Moran's I")
    # ax.set_ylabel("Density")
    # plt.show()

    print(pd.value_counts(lisa.q))
    # Divides the states into 4 classes based on the local Moran's I
    # 1. HH: High-High
    # 2. LL: Low-Low
    # 3. LH: Low-High
    # 4. HL: High-Low

    # Lisa Cluster Map
    # Plot legend as 1 -> HH, 2 -> LL, 3 -> LH, 4 -> HL
    lisa_cluster = {
        1: "HH",
        2: "LL",
        3: "LH",
        4: "HL",
    }

    # Plot the clusters
    fig, ax = plt.subplots(figsize=(12, 10))
    merged_df.assign(cl=lisa.q).plot(
        column="cl",
        categorical=True,
        k=4,
        cmap="RdBu",
        linewidth=0.8,
        ax=ax,
        edgecolor="white",
        legend=True,
        legend_kwds={
            "title": "Cluster",
            "labels": lisa_cluster.values(),
            "loc": "lower left",
        },
    )
    ax.set_axis_off()
    plt.show()
