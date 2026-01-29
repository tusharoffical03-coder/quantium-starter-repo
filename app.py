import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# ==============================
# READ & PREPARE DATA
# ==============================

df = pd.read_csv("output.csv")

# Standardise columns
df.columns = df.columns.str.lower().str.strip()

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"])

# Standardise region values
df["region"] = df["region"].astype(str).str.lower().str.strip()

# ==============================
# CREATE DASH APP
# ==============================

app = Dash(__name__)

app.layout = html.Div(className="container", children=[

    html.H1("Pink Morsels Sales Visualiser", className="title"),

    html.Div(className="controls", children=[
        html.Label("Select Region:", className="label"),

        dcc.RadioItems(
            id="region-selector",
            options=[
                {"label": "All", "value": "all"},
                {"label": "North", "value": "north"},
                {"label": "East", "value": "east"},
                {"label": "South", "value": "south"},
                {"label": "West", "value": "west"},
            ],
            value="all",
            inline=True
        )
    ]),

    dcc.Graph(id="sales-graph")
])

# ==============================
# CALLBACK
# ==============================

@app.callback(
    Output("sales-graph", "figure"),
    Input("region-selector", "value")
)
def update_graph(selected_region):

    # Filter by region
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    # Aggregate sales by date
    grouped_df = (
        filtered_df
        .groupby("date", as_index=False)
        .agg({"sales": "sum"})
        .sort_values("date")
    )

    # Create line chart
    fig = px.line(
        grouped_df,
        x="date",
        y="sales",
        title="Daily Total Sales Over Time",
        labels={
            "date": "Date",
            "sales": "Total Sales"
        }
    )

    return fig

# ==============================
# RUN SERVER
# ==============================

if __name__ == "__main__":
    app.run(debug=True)
