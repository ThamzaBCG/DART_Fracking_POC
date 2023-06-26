from typing import List

import dash_bootstrap_components as dbc
from dash import html

from dashboard.components.custom_ui_component import CustomUIComponent

class SidebarSubMenu(CustomUIComponent):
    def __init__(self, links: List[dbc.NavLink], id: str, title: str, id_submenu_content=None):
        self._content = html.Li(
            [
                dbc.NavLink(
                    [
                        title,
                        html.Span(className="bi-caret-down-fill"),
                    ],
                    href="#",
                    active="exact",
                    id=id,
                ),
                html.Ul(
                    links,
                    id=id_submenu_content,
                    hidden=False,
                ),
            ],
        )
