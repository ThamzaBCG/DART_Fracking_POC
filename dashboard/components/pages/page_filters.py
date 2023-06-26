from typing import Any, List

import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import MATCH, Input, Output, State

from dashboard.app import GLOBAL_FONT_FAMILY, app
from dashboard.components.custom_ui_component import CustomUIComponent


class PageFilter(CustomUIComponent):
    def __init__(self, children: Any, label: str, size: int = 3):
        self._content = children
        self.label = label
        self.size = size


class ModalDescription(CustomUIComponent):
    def __init__(self, description: List[str], index: str):
        self._content = html.Div(
            [
                html.I(
                    id={
                        "role": "open",
                        "index": index,
                    },
                    n_clicks=0,
                    className="bi bi-plus-square",
                    style={
                        "cursor": "pointer",
                        "padding-left": "6px",
                        "align-items": "center",
                    },
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Description")),
                        dbc.ModalBody(
                            description,
                            style={
                                "line-height": "1.8",
                            },
                        ),
                        dbc.ModalFooter(),
                    ],
                    id={
                        "role": "modal",
                        "index": index,
                    },
                    size="lg",
                    is_open=False,
                    backdrop=False,
                ),
            ],
            style={
                "margin-top": "1px",
            },
        )


@app.callback(
    Output({"role": "modal", "index": MATCH}, "is_open"),
    [
        Input({"role": "open", "index": MATCH}, "n_clicks"),
    ],
    [State({"role": "modal", "index": MATCH}, "is_open")],
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


class PageFiltersCard(CustomUIComponent):
    def __init__(
        self,
        children: List[PageFilter],
        title: str,
        description: ModalDescription = None,
    ):
        """
        Create a dbc.Row containing a dbc.Card component based on a list of
        PageFilter components.

        :param id: Identifier of the component
        :type id: str
        :param title: Title of the Card
        :type title: str
        :param children: List of PageFilter components, usually a dcc.Dropdown and a column size
        :type children: List[PageFilter]
        :param button_id: Identifier of the filter button
        :type button_id: str
        """
        self._content = dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            [
                                html.H5(
                                    title,
                                    style={
                                        "align-items": "center",
                                        "display": "flex",
                                        "margin-bottom": "2px",
                                        "font-family": GLOBAL_FONT_FAMILY,
                                    },
                                ),
                                description.content if description else None,
                            ],
                            class_name="d-flex",
                        ),
                        dbc.CardBody(
                            dbc.Row(
                                list(map(self._col_wrapper, children)),
                            )
                        ),
                    ],
                    class_name="border-primary p-0",
                )
            ),
            class_name="sticky-top",
            style={
                "top": "60px",
            },
        )

    @staticmethod
    def _col_wrapper(child: PageFilter) -> dbc.Col:
        try:
            col_to_return = dbc.Col(
                html.Div(
                    [
                        dbc.Label(
                            child.label,
                        ),
                        child.content,
                    ]
                ),
                class_name=f"col-lg-{child.size}",
            )
        except AttributeError:
            col_to_return = dbc.Col(
                html.Div([child]),
                class_name="col-lg",
            )
        return col_to_return