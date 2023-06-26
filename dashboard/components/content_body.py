from typing import List, Union

import dash_bootstrap_components as dbc
from dash import html

from dashboard.components.custom_ui_component import CustomUIComponent
from dashboard.components.pages.page import PageRow
from dashboard.components.pages.page_filters import PageFiltersCard

class ContentBody(CustomUIComponent):
    def __init__(self, page: List[Union[PageFiltersCard, PageRow, dbc.Tabs]], id: str):
        self._content = html.Div(
            page,
            id=id,
            hidden=False,
            style={
                "padding-top": "3em",
                "padding-bottom": "1em",
            },
            className="content-body",
        )
