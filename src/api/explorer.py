from tkinter import Y
import numpy as np
import streamlit as st
import plotly.express as px

from src.model import Customer


def emission_x_capture(df_copy):
    df = df_copy.copy()
    countries = ["Global"] + list(df.query_country.unique())
    country = st.selectbox("Country to analyse", countries, key=3)
    scope_options = ["Scope 1", "Scope 2", "Scope 3"]
    scopes = st.multiselect("Scopes to visualize", scope_options, default=scope_options)
    if country == "Global":
        df_country = df.copy()
    else:
        df_country = df.loc[df.query_country == country]
    del df
    df_country["emission"] = 0
    for idx in range(1, 4):
        if f"Scope {idx}" in scopes:
            df_country["emission"] += df_country[f"scope_{idx}_y0"]

    _emission_x_credits(df_country, country)
    _emission_x_ratio(df_country, country)
    _emission_without_credits(df_country, country)


def _emission_x_credits(df_country, country):
    cols_credits = [f"credits_{idx}" for idx in range(1, 5)]
    df_country["credits"] = df_country[cols_credits].sum(axis=1)
    df_country["credits / emission"] = (
        100 * df_country["credits"] / df_country["emission"]
    ).round(2).astype(str) + " %"
    dict_hover = dict(zip(df_country.columns, [False] * df_country.shape[1]))
    dict_hover.update({"emission": ":,", "credits": ":,", "credits / emission": True})
    fig = px.scatter(
        df_country,
        x="emission",
        y="credits",
        log_x=True,
        log_y=True,
        hover_name="company_name",
        hover_data=dict_hover,
    )
    fig.update_layout(
        width=800,
        title=f"{country} Companies",
        xaxis_title="Emissions (tCO2/y, log-scale)",
        yaxis_title="Credits (log-scale)",
    )
    st.plotly_chart(fig)


def _emission_x_ratio(df_country, country):
    df_country["credits / emission"] = df_country["credits"] / df_country["emission"]
    df_country["credits / emission."] = (100 * df_country["credits / emission"]).round(
        2
    ).astype(str) + " %"
    dict_hover = dict(zip(df_country.columns, [False] * df_country.shape[1]))
    dict_hover.update(
        {"credits": ":,.0f", "emission": ":,.0f", "credits / emission.": True}
    )
    fig = px.scatter(
        df_country,
        x="emission",
        y="credits / emission",
        log_x=True,
        log_y=True,
        hover_name="company_name",
        hover_data=dict_hover,
    )
    fig.update_layout(
        width=800,
        title=f"{country} Companies",
        xaxis_title="Emission (tCO2/y, log-scale)",
        yaxis_title="Credits / Emission (%)",
    )
    st.plotly_chart(fig)


def _emission_without_credits(df_country, country):
    df_country["random_y_index"] = np.random.rand((df_country.shape[0]))
    dict_hover = dict(zip(df_country.columns, [False] * df_country.shape[1]))
    dict_hover["emission"] = ":,.0f"
    fig = px.scatter(
        df_country,
        x="emission",
        y="random_y_index",
        hover_data=dict_hover,
        log_x=True,
        hover_name="company_name",
    )
    fig.update_layout(
        width=800,
        height=300,
        title=f"{country} Companies without carbon credits",
        xaxis_title="Emissions (tCO2/y, log-scale)",
        yaxis_showticklabels=False,
        yaxis_visible=False,
    )
    st.plotly_chart(fig)


def individual_company(df):
    company_name = st.text_input("Company to display", "EDF")
    df_company = df.loc[df.company_name == company_name]
    if df_company.shape[0] > 0:
        cols = df_company.columns
        v = df_company.values[0]
        item = dict(zip(cols, v))
        customer = Customer(**item).dict()
        st.json(customer)
