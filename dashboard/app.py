
import click
import dash
import plotly.io as pio

from .color_palette import color_palette
from dashboard.themes.theme_factory import ThemeFactory
from dashboard.themes.themes import(
    DARK_THEMES,
    darkly_theme,
    flatly_theme,
    pulse_theme,
    sandstone_theme,
    slate_theme,
    solar_theme,
    spacelab_theme,
)

DEFAULT_MULTI_ROW_HEIGHT = 350
GLOBAL_FONT_FAMILY = "Roboto"
GLOBAL_FONT = {
    "titlefont": {"size": 20},
    "font": {"size": 14},
    "font_family": GLOBAL_FONT_FAMILY,
}
# Set custom css and fonts
FONTS = "https://fonts.googleapis.com/css2?family=Roboto&display=swap"
BS_ICONS = "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.1/font/bootstrap-icons.css"
CUSTOM_LAYOUT = "/static/css/01_layout.css"

ui_theme = "flatly"

def setup(ui_theme, debug):
    theme = ThemeFactory.create(ui_theme)
    pio.templates.default = theme.plotly_template
    color_palette.set_colors(theme.colors)

    global EMPTY_PLOTLY_FIGURE
    EMPTY_PLOTLY_FIGURE = {
        "layout": {
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "annotations": [
                {
                    "text": "No matching data found",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 28},
                }
            ],
            "paper_bgcolor": "black" if ui_theme in DARK_THEMES else "white",
            "plot_bgcolor": "black" if ui_theme in DARK_THEMES else "white",
        }
    }

    global app
    app = dash.Dash(
            __name__,
            external_stylesheets=[
                theme.bootstrap_theme,
                BS_ICONS,
                FONTS,
                CUSTOM_LAYOUT,
                theme.color_css,
            ],
    )
    return app

