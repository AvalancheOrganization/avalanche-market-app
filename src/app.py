import pandas as pd
import numpy as np
import json

import streamlit as st

from src.db import fetch_db
import src.config as config

from src.api.overview import head_metrics, country_volume
from src.api.emissions import country_emission, ratio_with_required_volume
from src.api.credits import credits_type
from src.api.explorer import emission_x_capture, individual_company


class App:
    def __init__(self) -> None:
        self.db_name = config.DB_NAME
        self.df = self.get_df()
        self.geodata = get_geodata()
        st.title("Avalanche Market")
        st.text("powered by CDP")
        add_space()

    def run(self) -> None:
        self.overview()
        self.emissions()
        self.credits()
        self.explorer()

    def overview(self):
        st.header("Overview")
        head_metrics(self.df)
        country_volume(self.df, self.geodata)
        add_space()

    def emissions(self):
        st.header("Emissions")
        country_emission(self.df)
        ratio_with_required_volume(self.df)
        add_space()

    def credits(self):
        st.header("Credits")
        credits_type(self.df)
        add_space()

    def explorer(self):
        st.header("Explorer")
        emission_x_capture(self.df)
        individual_company(self.df)

    @st.cache(ttl=24 * 60 * 60 * 7)
    def get_df(self) -> pd.DataFrame:
        items = fetch_db(self.db_name)
        df = pd.DataFrame(items)
        df = transform(df)
        return df


@st.cache(allow_output_mutation=True)
def get_geodata():
    return json.load(open("data/countries.geojson"))


def transform(df):

    cols_scope_3 = config.CDP_SCOPE_3_MAPPING.values()
    cols_to_fill = [
        "scope_1_y0",
        "scope_2_location_y0",
        "scope_2_market_y0",
        *cols_scope_3,
    ]
    df[cols_to_fill].fillna(0, inplace=True)

    # scope 2 and 3
    df["scope_2_y0"] = df["scope_2_location_y0"] + df["scope_2_market_y0"]
    df["scope_3_y0"] = df[cols_scope_3].sum(axis=1)

    df["scope 1 + 2"] = df["scope_1_y0"] + df["scope_2_y0"]
    df["scope 1 + 2 + 3"] = df["scope 1 + 2"] + df["scope_3_y0"]

    # country
    countries = set(df.query_country.unique())
    mapping_countries = {c: c for c in countries}
    mapping_countries[
        "United Kingdom of Great Britain and Northern Ireland"
    ] = "United Kingdom"
    df["query_country"] = df["query_country"].map(mapping_countries)

    return df


def add_space():
    st.markdown("<br><br>", unsafe_allow_html=True)


# def country_emission(df):
#     # df_sum = (
#     #    df[["query_country", "scope_1_y0"]].groupby("query_country").sum().reset_index()
#     # )
#     countries, emissions = [], []
#     for this_country, this_df in df[["query_country", "scope_1_y0"]].groupby(
#         "query_country"
#     ):
#         this_df = this_df.loc[this_df.scope_1_y0 > 0]
#         y = np.log(this_df.scope_1_y0.values)
#         emissions.append(y)
#         countries.append(this_country)
#     fig = ff.create_distplot(emissions, countries)
#     st.plotly_chart(fig)
