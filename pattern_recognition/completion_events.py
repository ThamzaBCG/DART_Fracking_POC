import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from src.config import config

import src.constants.datasets as ds
import src.constants.query_parameters as q
import src.constants.general as g
import src.constants.completion_columns as cc

from src.plot_utils import completion_plot_events


# Crear DataFrame de ejemplo
df = pd.read_csv(config.output_dir / "completion_pattern_recognition.csv")

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Definir el diseño de la aplicación
app.layout = html.Div([
    html.H1(f"Asset: {df[cc.ASSET_ID].unique()[0]}"),
    html.Div([
        html.Label('Select Stage:'),
        dcc.RadioItems(
            id='filtro-categoria',
            options=[{'label': categoria, 'value': categoria} for categoria in df[cc.STAGE_NUMBER].unique()],
            value=df[cc.STAGE_NUMBER].unique()[0],
            labelStyle={'display': 'inline-block', 'margin-right': '10px', 'color': 'black'}
        ),
    ]),
    dcc.Graph(id='grafica')
])

# Definir el callback para actualizar la gráfica según el filtro
@app.callback(
    dash.dependencies.Output('grafica', 'figure'),
    [dash.dependencies.Input('filtro-categoria', 'value')]
)
def update_graph(categoria):
    filtered_df = df[df[cc.STAGE_NUMBER] == categoria]

    figure = completion_plot_events(filtered_df)

    return figure

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
