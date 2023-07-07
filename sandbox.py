from typing import List

import plotly
import contextily

import pandas as pd
import geopandas as gpd
import geoplot as gplot
import geoplot.crs as gcrs
import matplotlib.pyplot as plt
import seaborn as sns

from pysal.lib import weights

from constants import DATA

if __name__ == "__main__":
    df = pd.read_csv(
        DATA / "CDC Injury Center Drug Overdose Deaths.csv", encoding="ISO-8859-1"
    )

    # print(df.info())

    sub_df = df.rename(
        columns={
            "2019 Age-adjusted Rate (per 100,000 population)": "2019",
            "2018 Age-adjusted Rate (per 100,000 population)": "2018",
            "2017 Age-adjusted Rate (per 100,000 population)": "2017",
            "2016 Age-adjusted Rate (per 100,000 population)": "2016",
            "2015 Age-adjusted Rate (per 100,000 population)": "2015",
            "2014 Age-adjusted Rate (per 100,000 population)": "2014",
            "2013 Age-adjusted Rate (per 100,000 population)": "2013",
        }
    )

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)

    sub_df = sub_df[
        [
            "State",
            "2019",
            "2018",
            "2017",
            "2016",
            "2015",
            "2014",
            "2013",
        ]
    ]

    # This says we have some missing values
    # print(df.isna().values.any())
    # Let's confirm where they are
    # print(df.isnull().sum())
    # Since, it's a small dataset of 50 rows, we can look their position
    # Looks like if we drop them we will be dropping District Of Columbia
    # at this state we can either fill it with mean, median, mode or
    # interpolate it.. or just drop it! Let's just drop it for now.
    sub_df = sub_df.dropna()
    # print(df.shape)

    sub_df = sub_df.set_index("State")

    # If I plot before this it is taking columns as y axis [years]
    # and we want the other way around.. so transpose
    transposed_df = sub_df.T
    # print(df.head())
    # print(transposed_df.head())

    # Also, it's showing 2019..2013, let's sort it
    transposed_df = transposed_df.sort_index()

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
