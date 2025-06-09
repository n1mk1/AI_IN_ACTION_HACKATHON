import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd
from pymongo import MongoClient
from waitress import serve
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
mapbox_token = os.getenv("MAPBOX_TOKEN")
px.set_mapbox_access_token(mapbox_token)

# MongoDB setup
ATLAS_URI = "mongodb+srv://as:<pass>@cluster0.7nmgzr1.mongodb.net/"
DB_NAME = "CovidDB"
NEIGHBOURHOODS_COL = "Neighbourhoods"
CASES_COL = "CovidCases"

mongo_client = MongoClient(ATLAS_URI)
db = mongo_client[DB_NAME]
neigh_collection = db[NEIGHBOURHOODS_COL]
cases_collection = db[CASES_COL]

# Define layout function to refresh data on each load
def serve_layout():
    # Load neighbourhood data
    neigh_df = pd.DataFrame(list(neigh_collection.find({}, {"_id": 0})))
    neigh_df = neigh_df.dropna(subset=["latitude", "longitude"])

    # Load COVID case counts
    case_counts = pd.DataFrame(list(cases_collection.aggregate([
        {"$group": {"_id": "$Neighbourhood_Name", "count": {"$sum": 1}}}
    ])))
    case_counts = case_counts.rename(columns={"_id": "neighbourhood", "count": "case_count"})

    # Merge into neighbourhood dataframe
    neigh_df = neigh_df.merge(case_counts, on="neighbourhood", how="left")
    neigh_df["case_count"] = neigh_df["case_count"].fillna(0)

    # Map figure using plotly scatter_mapbox
    # Map figure using plotly scatter_mapbox
    fig = px.scatter_mapbox(
        neigh_df,
        lat="latitude",
        lon="longitude",
        color="case_count",
        size="case_count",
        hover_name="neighbourhood",
        zoom=10,
        height=700,
        title="Toronto Neighbourhood COVID-19 Cases",
        mapbox_style="mapbox://styles/mapbox/dark-v10"  # Fancy dark style
    )
    fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})

    # Layout
    return html.Div([
        html.H2("Toronto COVID-19 Dashboard", style={"textAlign": "center"}),

        html.Div([
            dcc.Graph(id="map", figure=fig, style={"flex": "2"}),

            html.Div([
                html.H4("COVID-19 Case Details"),
                dash_table.DataTable(
                    id="case-table",
                    columns=[
                        {"name": "Gender", "id": "Client_Gender"},
                        {"name": "Age Group", "id": "Age_Group"},
                        {"name": "Episode Date", "id": "Episode_Date"},
                        {"name": "Reported Date", "id": "Reported_Date"},
                        {"name": "Classification", "id": "Classification"},
                        {"name": "Outcome", "id": "Outcome"},
                        {"name": "Source", "id": "Source_of_Infection"},
                    ],
                    data=[],
                    page_size=15,
                    style_table={"overflowY": "scroll", "maxHeight": "700px"},
                    style_cell={"textAlign": "left", "padding": "5px"},
                    style_header={"backgroundColor": "#f2f2f2", "fontWeight": "bold"},
                    style_data={"whiteSpace": "normal", "height": "auto"},
                )
            ], style={
                "flex": "1",
                "padding": "20px",
                "background": "#f9f9f9",
                "borderLeft": "1px solid #ccc"
            })
        ], style={"display": "flex", "flexDirection": "row"})
    ])

# Initialize Dash app with dynamic layout
app = dash.Dash(__name__)
app.title = "Toronto COVID Map"
app.layout = serve_layout  # <-- KEY: dynamic layout loaded on every page refresh

# Callback to update table when a point is clicked
@app.callback(
    Output("case-table", "data"),
    Input("map", "clickData")
)
def update_table(clickData):
    if not clickData:
        return []

    neighbourhood = clickData["points"][0]["hovertext"]
    cursor = cases_collection.find({"Neighbourhood_Name": neighbourhood}, {"_id": 0})
    return list(cursor)

# Run with Waitress
if __name__ == "__main__":
    serve(app.server, host="0.0.0.0", port=8052)
