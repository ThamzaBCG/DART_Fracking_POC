import logging
from typing import List

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots

from dashboard.app import (
    DEFAULT_MULTI_ROW_HEIGHT,
    EMPTY_PLOTLY_FIGURE,
    GLOBAL_FONT,
    app,
    color_palette,
)
from dashboard.components.content_body import ContentBody
from dashboard.components.pages.page import PageCol, PageRow
from dashboard.components.pages.page_filters import (
    ModalDescription,
    PageFilter,
    PageFiltersCard
)

pd.options.mode.chained_assignment = None  # default='warn'

def historical_features():
    df = px.data.carshare()

    fig = px.scatter_mapbox(df, lat="centroid_lat", lon="centroid_lon", color="peak_hour", size="car_hours",
                    color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
                    mapbox_style="carto-positron")
    
    return fig

def get_tab2():
    id_content = "tab2-content"
    content = html.Div(id=id_content)
    
    tab2_filters = [
    ]

    tab2_fil = [
        PageFiltersCard(tab2_filters, "Car Sharing Map").content,
        PageRow(
            [
                PageCol(
                    dcc.Graph(figure=historical_features()),
                    15,
                ),
            ]
        ).content,
    ]

    content = ContentBody(
        [dbc.Tab(tab2_fil, label="tab2", style={"margin-bottom": "1em"})],
        id=id_content,
    ).content
    return content

TAB2_CONTENT = get_tab2()


# -------- Table functions -----

# @app.callback(
#     Output("tab2-view", "figure"),
#     Input("filter21", "value"),
# )
# def historical_features():
#     df = px.data.carshare()

#     fig = px.scatter_mapbox(df, lat="centroid_lat", lon="centroid_lon", color="peak_hour", size="car_hours",
#                     color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
#                     mapbox_style="carto-positron")
    
#     return fig


@app.callback(
    Output("tab2-content", "hidden"),
    Input("url", "pathname"),
)
def display_response_model_content(pathname):
    return False if "pages/tab2" in pathname else True