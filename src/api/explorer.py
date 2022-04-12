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
    cols_credits = [f"credits_{idx}" for idx in range(1, 5)]

    df_country["y"] = 0
    for idx in range(1, 4):
        if f"Scope {idx}" in scopes:
            df_country["y"] += df_country[f"scope_{idx}_y0"]

    df_country["credits"] = df_country[cols_credits].sum(axis=1)
    fig = px.scatter(
        df_country,
        x="y",
        y="credits",
        log_x=True,
        log_y=True,
        hover_name="company_name",
    )
    fig.update_layout(
        title=f"{country} Companies",
        xaxis_title="Emissions (tCO2/y, log-scale)",
        yaxis_title="Credits (log-scale)",
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
