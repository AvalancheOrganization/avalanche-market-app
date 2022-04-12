from copy import deepcopy
import pydeck as pdk
import streamlit as st
import plotly.express as px


def head_metrics(df):
    countries = df.query_country.unique()
    df_having_credits = df.loc[df.credits_1.notnull()]
    having_credits = round(len(df_having_credits) / len(df) * 100, 2)
    col1, col2, col3 = st.columns(3)
    col2.metric("Countries", len(countries), delta=3)
    col1.metric("Companies", len(df), delta=1200)
    col3.metric("% having CRC credits", having_credits)


def country_volume(df, geodata_copy):
    geodata = deepcopy(geodata_copy)
    countries = set(df.query_country.unique())
    for row in geodata["features"]:
        this_country = row["properties"]["ADMIN"]
        if this_country in countries:
            # volume = df.loc[df.query_country == this_country].shape[0]
            color = [18, 7, 252]
        else:
            color = [0, 0, 0]
        row["properties"]["color"] = color  # volume / max_volume * 255

    layer_geojson = pdk.Layer(
        "GeoJsonLayer",
        geodata,
        opacity=0.8,
        filled=True,
        wireframe=True,
        stroked=False,
        extruded=True,
        get_fill_color="properties.color",
    )
    initial_view_state = pdk.ViewState(
        latitude=48.86,
        longitude=2.34,
        zoom=0.5,
        min_zoom=0.5,
        max_zoom=0.5,  # 2
        pitch=45,
        bearing=0,
    )
    r = pdk.Deck(
        layers=[layer_geojson],
        initial_view_state=initial_view_state,
        map_provider=None,
        width=2000,
        height=1200,
    )  # map_style="light")
    st.pydeck_chart(r, use_container_width=False)

    df_count = (
        df[["query_country", "query_year"]]
        .groupby("query_country")
        .count()
        .reset_index()
    )
    df_count.rename(
        columns={"query_country": "Country", "query_year": "Total"}, inplace=True
    )
    df_count.sort_values("Total", ascending=False, inplace=True)
    # fig = go.Figure(go.Bar(x=df_count["Country"], y=df_count["Total"]))
    fig = px.bar(df_count, x="Country", y="Total", color="Total")
    fig.update_layout(title="Number of companies registered in the CDP, by country")
    st.plotly_chart(fig)
