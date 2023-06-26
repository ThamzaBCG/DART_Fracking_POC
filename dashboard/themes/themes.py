from dataclasses import dataclass
from typing import List

import dash_bootstrap_components as dbc
import plotly.express as px

@dataclass
class Theme:
    name: str
    colors: List[str]
    bootstrap_theme: str
    plotly_template: str
    color_css: str


BCG_COLOR_PALETTE = [
    "#03fc84",
    "#146145",
    "#5188c8",
    "#c7c7c7",
    "#45cee3",
    "#875484",
    "#ea5353",
    "#bf6363",
    "#1a94a0",
    "#94a0b7",
    "#becc72",
    "#3709d1",
]

flatly_theme = Theme(
    name="flatly",
    colors=px.colors.qualitative.T10,
    bootstrap_theme=dbc.themes.FLATLY,
    plotly_template="plotly_white",
    color_css="/static/css/02_light.css",
)

darkly_theme = Theme(
    name="darkly",
    colors=BCG_COLOR_PALETTE,
    bootstrap_theme=dbc.themes.DARKLY,
    plotly_template="plotly_dark",
    color_css="/static/css/02_dark.css",
)

slate_theme = Theme(
    name="slate",
    colors=BCG_COLOR_PALETTE,
    bootstrap_theme=dbc.themes.SLATE,
    plotly_template="plotly_dark",
    color_css="/static/css/02_dark.css",
)

sandstone_theme = Theme(
    name="sandstone",
    colors=px.colors.qualitative.T10,
    bootstrap_theme=dbc.themes.SANDSTONE,
    plotly_template="plotly_white",
    color_css="/static/css/02_light.css",
)

solar_theme = Theme(
    name="solar",
    colors=px.colors.qualitative.T10,
    bootstrap_theme=dbc.themes.SOLAR,
    plotly_template="plotly_white",
    color_css="/static/css/02_light.css",
)

pulse_theme = Theme(
    name="pulse",
    colors=px.colors.qualitative.T10,
    bootstrap_theme=dbc.themes.PULSE,
    plotly_template="plotly_white",
    color_css="/static/css/02_light.css",
)

spacelab_theme = Theme(
    name="spacelab",
    colors=px.colors.qualitative.T10,
    bootstrap_theme=dbc.themes.SPACELAB,
    plotly_template="plotly_white",
    color_css="/static/css/02_light.css",
)

DARK_THEMES = [darkly_theme.name, slate_theme.name]
