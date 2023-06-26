from typing import Any, List

import dash_bootstrap_components as dbc
from dash import dcc

from dashboard.components.custom_ui_component import CustomUIComponent


class PageCol(CustomUIComponent):
    def __init__(self, children: Any, size: int):
        self._content = children
        self.size = size


class PageRow(CustomUIComponent):
    def __init__(self, children: List[PageCol], style=None):
        """Create un dbc.Row component based on a list of Charts and their size.

        :param children: A list of PageCol components that usually contain a chart.
        Charts are mainly dcc.Graph but can whatever content that fits in a dcc.Col
        :type children: List[PageCol]
        """
        if style is None:
            style = {"margin-top": "0em"}

        self._content = dbc.Row(
            list(map(self._col_wrapper, children)),
            class_name="gx-3 gy-3",
            style=style,
        )

    @staticmethod
    def _col_wrapper(child: PageCol) -> dbc.Col:
        shadow_class = "shadow-sm"
        html_class_attr = "className"

        # Remove plotly logo on all charts
        if isinstance(child.content, dcc.Graph):
            try:
                child.content.config["displaylogo"] = False
            except AttributeError:
                child.content.config = {"displaylogo": False}

        # Add the shadow effect class to the dbc.Col child
        if html_class_attr in child.content.available_properties:
            class_value = getattr(child.content, html_class_attr, "") + shadow_class
            setattr(child.content, html_class_attr, class_value)

        return dbc.Col(
            child.content,
            class_name=f"col-lg-{child.size} img-hover-zoom rounded",
        )