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
    required_volume = st.number_input(
        "Required volume of CO2", min_value=1, value=config.WOOD_MASS_YEARLY
    )
    countries = ["Global"] + list(df.query_country.unique())
    country = st.selectbox("Country to analyse", countries, key=1)
    if country == "Global":
        df_country = df.copy()
    else:
        df_country = df.loc[df.query_country == country]
    del df

    df_sums = [
        _get_required_volume(df_country[["company_name", col]], required_volume)
        for col in ["scope_1_y0", "scope 1 + 2", "scope 1 + 2 + 3"]
    ]
    df_cumsums = [_get_cumulative_volume(df) for df in df_sums]
    titles = [
        f"{country} {name}" for name in ["scope 1", "scope 1 + 2", "scope 1 + 2 + 3"]
    ]
    _display_sum(df_sums, titles)
    _display_cumsum(df_cumsums, titles)


def _display_sum(df_sums, titles):
    fig = go.Figure()
    for title, df in zip(titles, df_sums):
        cols = df.columns
        company_names = df.company_name.values
        fig.add_trace(
            go.Scatter(
                x=list(range(len(df))),
                y=df[cols[1]],
                name=title,
                hovertemplate="<b>%{text}</b><br>emission ratio: %{y}",
                text=company_names,
            )
        )
    fig.update_traces(mode="markers")
    fig.update_layout(
        title="Sum of ratio",
        width=800,
        height=500,
        yaxis_type="log",
        xaxis_title="Number of companies",
    )
    st.plotly_chart(fig)


def _display_cumsum(df_cumsums, titles):
    fig = go.Figure()
    for title, df in zip(titles, df_cumsums):
        cols = df.columns
        company_names = df.company_name.values
        fig.add_trace(
            go.Scatter(
                x=list(range(len(df))),
                y=df[cols[1]],
                name=title,
                hovertemplate="<b>%{text}</b><br>cumulative emission ratio: %{y}",
                text=company_names,
            )
        )
    fig.update_traces(mode="markers")
    fig.update_layout(
        title="Cumulative sum of ratio",
        width=800,
        height=500,
        yaxis_type="log",
        xaxis_title="Number of companies",
    )
    st.plotly_chart(fig)


def _get_required_volume(df, required_volume):
    cols = df.columns
    df[cols[1]] = df[cols[1]] / required_volume
    df.sort_values(cols[1], inplace=True)
    return df


def _get_cumulative_volume(df):
    df_copy = df.copy()
    cols = df_copy.columns
    df_copy[cols[1]] = df_copy[cols[1]].cumsum()
    return df_copy
