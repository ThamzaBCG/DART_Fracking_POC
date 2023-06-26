import dash_bootstrap_components as dbc
from dash import dcc, html

from dashboard.components.navbar import NAVBAR
from dashboard.components.sidebar import SIDEBAR

from dashboard.components.pages.tabs.tab1 import TAB1_CONTENT
from dashboard.components.pages.tabs.tab2 import TAB2_CONTENT


content = dbc.Col(
    [
        TAB1_CONTENT,
        TAB2_CONTENT
    ],
    class_name="col-lg-10",
)

content_container = dbc.Container(
    dbc.Row(
        [SIDEBAR, content],
        style={"margin-top": "30px"},
        class_name="flex-nowrap",
    ),
    fluid=True,
)

# Main layout
main_layout = html.Div(
    [
        dcc.Location(
            id="url",
            refresh=False
        ),
        NAVBAR,
        content_container
    ]
)
