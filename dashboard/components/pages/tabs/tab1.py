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

def get_tab1():
    id_content = "tab1-content"
    content = html.Div(id=id_content)
    
    features_fit = [
        PageFilter(
                dcc.Dropdown(
                    id="filter1",
                    options=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'],
                    value=['sepal_length', 'sepal_width'],
                    multi=True
                ),
                "Dimensions",
                6
        ),
    ]

    features = [
        PageFiltersCard(features_fit, "Iris Scatter").content,
        PageRow(
            [
                PageCol(
                    dcc.Graph(id="tab1-view"),
                    15,
                ),
            ]
        ).content,
    ]

    content = ContentBody(
        [dbc.Tab(features, label="tab1", style={"margin-bottom": "1em"})],
        id=id_content,
    ).content
    return content

TAB1_CONTENT = get_tab1()


# -------- Table functions -----

@app.callback(
    Output("tab1-view", "figure"),
    Input("filter1", "value"),
)
def historical_features(dims):
    df = px.data.iris()
    fig = px.scatter_matrix(
        df, 
        dimensions=dims, 
        color="species"
    )
    
    return fig


@app.callback(
    Output("tab1-content", "hidden"),
    Input("url", "pathname"),
)
def display_response_model_content(pathname):
    return False if "pages/tab1" in pathname else True