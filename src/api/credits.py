import pandas as pd
import streamlit as st
import plotly.express as px


def credits_type(df):
    countries = ["Global"] + list(df.query_country.unique())
    country = st.selectbox("Country to analyse", countries, key=2)
    if country == "Global":
        df_country = df.copy()
    else:
        df_country = df.loc[df.query_country == country]
    df_credits = _melt_credits(df_country)

    credits_by_standards(df_credits)
    credits_by_ghg_scope(df_country, df_credits)


def _melt_credits(df_country):
    """
    Melt 4 credits columns into a single one.
    """
    cols = [f"verify_standards_{idx}" for idx in range(1, 5)]
    dfs = []
    for idx in range(1, 5):
        cols = [f"verify_standards_{idx}", f"credits_{idx}", "company_name"]
        this_df = df_country[cols].rename(
            columns=dict(zip(cols, ["verify_standards", "credits"]))
        )
        dfs.append(this_df)
    df_credits = pd.concat(dfs)
    df_credits = df_credits.loc[df_credits.verify_standards.notnull()]
    return df_credits


def credits_by_standards(df_credits):
    df_credits_copy = df_credits.copy()
    df_credits_copy = _map_credits(df_credits_copy)
    df_sum = df_credits_copy.groupby("verify_standards").sum().reset_index()
    df_sum = df_sum.sort_values("credits", ascending=False)
    fig = px.bar(
        df_sum,
        x="verify_standards",
        y="credits",
        color="credits",
        hover_name="verify_standards",
        hover_data={"credits": ":,.2f", "verify_standards": False},
    )
    # fig.update_layout(width=1000, height=800)
    fig.update_layout(title="Credits Volume by Verify Standards")
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)


def _map_credits(df_credits):
    """
    Clean verify standards by remapping them.
    """
    mapping_standards = {
        "VCS": "VCS (Verified Carbon Standard)",
        "Gold Standard": "Gold Standard",
        "CDM": "CDM (Clean Development Mechanism)",
        "CAR": "CAR (The Climate Action Reserve)",
        "ACR": "(American Carbon Registry)",
        "CCBS": "CCBS",
        "Alberta": "Alberta CIR",
        "Not yet verified": "Not yet verified",
        "Vivo": "Plan Vivo",
        "Others": "Others",
    }
    cols = df_credits.columns
    col2idx = dict(zip(cols, range(len(cols))))
    results = []
    for row in df_credits.values:
        for sd in mapping_standards:
            if sd in row[col2idx["verify_standards"]]:
                row[col2idx["verify_standards"]] = sd
                break
        else:
            row[col2idx["verify_standards"]] = "Others"
        results.append(dict(zip(cols, row)))
    df_credits = pd.DataFrame(results)
    df_credits = df_credits.loc[
        df_credits.verify_standards.isin(list(mapping_standards))
    ]
    df_credits["verify_standards"] = df_credits.verify_standards.map(mapping_standards)
    return df_credits


def credits_by_ghg_scope(df_country, df_credits):
    df_credits_copy = df_credits.copy()
    df_credits_copy = _map_ghg(df_country, df_credits_copy)
    df_ghg = df_credits_copy.groupby("ghg_scope").sum().reset_index()
    scopes = [
        "Scope 1",
        "Scope 2",
        "Scope 3",
        "Scope 1, Scope 2",
        "Scope 1, Scope 3",
        "Scope 2, Scope 3",
        "Scope 1, Scope 2, Scope 3",
    ]
    mapping_scope_order = dict(zip(scopes, list(range(len(scopes)))))
    df_ghg["order"] = df_ghg.ghg_scope.map(mapping_scope_order)
    df_ghg.sort_values("order", inplace=True)
    fig = px.bar(
        df_ghg,
        x="ghg_scope",
        y="credits",
        color="credits",
        hover_name="ghg_scope",
        hover_data={"credits": ":,.2f", "ghg_scope": False, "order": False},
    )
    fig.update_layout(title="Credits Volume by GHG Scope")
    st.plotly_chart(fig)


def _map_ghg(df_country, df_credits):
    df_credits = df_credits.groupby("company_name").sum().reset_index()
    name2ghg_scope = (
        df_country[["company_name", "ghg_scope"]]
        .set_index("company_name")
        .to_dict("index")
    )
    mapping_ghg = {k: v["ghg_scope"] for k, v in name2ghg_scope.items()}
    df_credits["ghg_scope"] = df_credits.company_name.map(mapping_ghg)
    return df_credits
