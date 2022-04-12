import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import numpy as np

import src.config as config


def country_emission(df):
    countries = (
        df.groupby("query_country")
        .count()
        .reset_index()
        .sort_values("query_year", ascending=False)
    ).query_country.values
    mapping_countries = dict(zip(countries, list(range(len(countries)))))
    data = []
    for idx in range(1, 4):
        col = f"scope_{idx}_y0"
        name = f"Scope {idx}"
        df_sum = df[["query_country", col]].groupby("query_country").sum().reset_index()
        df_sum["order"] = df_sum["query_country"].map(mapping_countries)
        df_sum.sort_values("order", inplace=True)
        emissions = df_sum[col].values
        data.append(go.Bar(name=name, x=countries, y=emissions))
    fig = go.Figure(data=data)
    fig.update_layout(
        title="Emissions by scope (2021)", barmode="group", yaxis_title="tCO2/y"
    )
    st.plotly_chart(fig)


def ratio_with_required_volume(df):
    st.subheader("Ratio with required volume")
    countries = ["Global"] + list(df.query_country.unique())
    country = st.selectbox("Country to analyse", countries, key=1)
    if country == "Global":
        df_country = df.copy()
    else:
        df_country = df.loc[df.query_country == country]

    serie_scopes = [
        _get_required_volume(df_country[col])
        for col in ["scope_1_y0", "scope 1 + 2", "scope 1 + 2 + 3"]
    ]
    titles = [
        f"{country} {name}" for name in ["scope 1", "scope 1 + 2", "scope 1 + 2 + 3"]
    ]
    fig = go.Figure()
    for title, serie in zip(titles, serie_scopes):
        fig.add_trace(go.Scatter(x=list(range(len(serie))), y=serie, name=title))
    fig.update_layout(width=800, height=600, yaxis_type="log")
    st.plotly_chart(fig)


def _get_required_volume(serie):
    # serie = serie.loc[serie > 0]
    return (serie / config.WOOD_MASS_YEARLY).sort_values(ascending=True).cumsum()
