import dash_bootstrap_components as dbc
from dash import html

from dashboard.components.sidebar_submenus.response_model_submenus import (
    RESPONSE_SUBMENUS,
)

SIDEBAR = dbc.Col(
    [
        dbc.Nav(
            [
                dbc.Button(
                    "Refresh datasets",
                    class_name="btn btn-primary btn-sm",
                    id="refresh-dataset-button",
                ),
                html.Hr(),
                html.Li(
                    dbc.NavLink(
                        ["Home"],
                        href="/",
                        active="exact",
                        className="nav-item",
                    ),
                ),
                RESPONSE_SUBMENUS,
            ],
            vertical=True,
        ),
    ],
    class_name="col-lg-2 sidebar-col shadow-sm",
    style={"min-height": "100vh", "min-width": "250px", "padding-top": "50px"},
)

