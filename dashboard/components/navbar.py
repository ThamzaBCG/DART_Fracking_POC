import dash
import dash_bootstrap_components as dbc
from dash import html

from dashboard.app import app
from dashboard.constants.constants import *

LOGO = app.get_asset_url(NAVBAR_LOGO)

NAVBAR = dbc.Navbar(
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        [
                            html.Img(
                                src=LOGO,
                                height="30px",
                                style={"margin-top": "-5px"},
                            ),
                            dbc.NavbarBrand(
                                DASHBOARD_TITLE,
                                style={"margin-left": "10px"},
                            ),
                        ],
                        href="/",
                        style={"textDecoration": "none", "margin-left": "1em"},
                    ),
                    class_name="col-lg-2",
                    style={"padding": "1em 0 0 0", "min-width": "250px"},
                ),
                # DEMAND_FORECAST_FILTERS,
                dbc.Col(
                    [
                        html.A(
                            html.Img(
                                src=dash.Dash("app").get_asset_url("question-circle.svg"),
                                height="30px",
                                width="30px",
                            ),
                            href=HELP_URL,
                            target="_blank",
                        ),
                    ],
                    id="help-link",
                    class_name="float-right",
                    style={"padding": "1em 1em 1em 0", "text-align": "right"},
                ),
            ],
            style={"height": "60px"},
            class_name="flex-nowrap",
        ),
        fluid=True,
        style={"display": "block"},
    ),
    color="primary",
    class_name="p-0 scroll",
    dark=True,
    fixed="top",
    style={"overflow": "visible"},
)
