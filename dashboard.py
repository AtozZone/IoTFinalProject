import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go
import dash_daq as daq
from dash.dependencies import Input, Output

#sets up the app and gets external css like bootstrap
app = dash.Dash(
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "/assets/style.css",
        "https://fonts.googleapis.com/css?family=Roboto",
    ]
)

#sidebar design
sidebar = html.Div(
    [
        html.H6("IoT", className="display-block text-center fs-1"),
        html.H6("Dashboard", className="display-block text-center fs-1"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/index", active="exact"),
                dbc.NavLink("Page 1", href="/page1", active="exact"),
                dbc.NavLink("Page 2", href="/page2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        dbc.NavLink(
            "Username",
            href="/login",
            active="exact",
            className="mt-auto text-center fs-3",
        ),
        dbc.NavLink("Logout", href="/index", active="exact", className="text-center py-3 fs-3"),
    ],
    className="sidebar d-flex flex-column flex-shrink-0 p-2 text-white bg-dark",
    style={
        "width": "15rem",
        "height": "100vh",
        "border": "0.5px solid gray",
    },
)


temp = 19
humi = 33
#gauge design
gauge = html.Div(
    [
        html.H3(
            "temperature",
            className="bold text-center p-4 text-light",
        ),
        daq.Gauge(
            id="temp-gauge",
            label={
                "label": "{:.2f}°C".format(temp), #gets temperature from static value
                "style": {
                    "fontSize": "20px",
                    "fontWeight": "bold",
                    "fontFamily": "Roboto, sans-serif",
                    "color": "white",
                },
            },
            color={
                "gradient": True,
                "ranges": {"#00C0F5": [0, 25], "#E3FC00": [25, 50], "#FFBB00": [50, 75], "red": [75, 100]},
            },
            value=temp,
            min=0,
            max=100,
            labelPosition="bottom",
            style={
                "textAlign": "center",
                "fontFamily": "Roboto, sans-serif",
                "color": "white",
            },
            scale=3,
            showCurrentValue=False,
        ),
        html.H3(
            "Humidity",
            className="bold text-center p-4 text-light",
        ),
        daq.Gauge(
            id="humi-gauge",
            label={
                "label": "{:}%".format(humi), #change temperature value here
                "style": {
                    "fontSize": "20px",
                    "fontWeight": "bold",
                    "fontFamily": "Roboto, sans-serif",
                    "color": "white",
                },
            },
            color={
                "gradient": True,
                "ranges": {"#00FFF7": [0, 33], "#00BBFF": [33, 66], "#0022FF": [66, 100]},
            },
            value=humi,
            min=0,
            max=100,
            labelPosition="bottom",
            style={
                "textAlign": "center",
                "fontFamily": "Roboto, sans-serif",
                "color": "white",
            },
            scale=3,
            showCurrentValue=False,
        ),
    ],
    className="text-light mx-5",
)

dcc.Interval(
    id='interval-component',
    interval=2 * 1000,  # updates every 2 seconds
    n_intervals=0
)

content = html.Div(
    [
        html.H2("Content", className="display-4"),
        html.Hr(),
        html.P("Welcome to the content area!"),
    ],
    style={"padding": "2rem"},
)

app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width="auto", style={"margin": "auto"}),
                dbc.Col(gauge, width="auto", style={"margin": "auto"}),
                dbc.Col(),
            ],
            style={"justify-content": "center", "align-items": "center"}
        )
    ],
    className="bg-dark",
)


if __name__ == "__main__":
    app.run(debug=True)
