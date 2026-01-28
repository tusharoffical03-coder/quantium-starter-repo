import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# Read data
df = pd.read_csv("output.csv")

# Convert date
df["date"] = pd.to_datetime(df["date"])

# Aggregate sales by date
df = df.groupby("date", as_index=False)["sales"].sum()

# Sort by date
df = df.sort_values("date")

# Line chart
fig = px.line(
    df,
    x="date",
    y="sales",
    title="Pink Morsels Sales Over Time",
    labels={
        "date": "Date",
        "sales": "Total Sales"
    }
)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsels Sales Visualiser"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
