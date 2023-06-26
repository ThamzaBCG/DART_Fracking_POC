from ctypes import POINTER

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from dashboard.app import app
from dashboard.components.sidebar_submenus.sidebar_submenus import SidebarSubMenu

def get_response_submenus():
    id_content = "Home-submenu"
    content = html.Div(id=id_content)
    
    links = [
        dbc.NavLink("Iris Scatter", href="/pages/tab1"),
        dbc.NavLink("Car Share Map", href="/pages/tab2"),
    ]
    content = SidebarSubMenu(
        links=links,
        id=id_content,
        title="Content",
        id_submenu_content="Home-submenu-content",
    ).content

    return content

RESPONSE_SUBMENUS = get_response_submenus()

@app.callback(
    Output("Home-submenu-content", "hidden"),
    [Input("Home-submenu", "n_clicks")],
    [State("Home-submenu-content", "hidden")],
)
def toogle_response_model_menu(n, status):
    return not status


