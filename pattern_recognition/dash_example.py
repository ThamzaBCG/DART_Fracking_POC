import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# Crear un DataFrame con los datos
data = {
    'País': ['Estados Unidos', 'Canadá', 'México', 'Brasil', 'India'],
    'Población': [331002651, 37742154, 128932753, 212559417, 1393409038],
    'Superficie': [9833517, 9976140, 1964375, 8515767, 3287263]
}
df = pd.DataFrame(data)

# Crear la aplicación Dash
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1("Información de Países"),
        dcc.Graph(
            figure={
                'data': [
                    {'x': df['País'], 'y': df['Población'], 'type': 'bar', 'name': 'Población'},
                    {'x': df['País'], 'y': df['Superficie'], 'type': 'bar', 'name': 'Superficie'}
                ],
                'layout': {
                    'title': 'Población y Superficie por País'
                }
            }
        ),
        html.Table(
            children=[
                html.Thead(
                    html.Tr(
                        children=[
                            html.Th('País'),
                            html.Th('Población'),
                            html.Th('Superficie')
                        ]
                    )
                ),
                html.Tbody(
                    [
                        html.Tr(
                            children=[
                                html.Td(df['País'][i]),
                                html.Td(df['Población'][i]),
                                html.Td(df['Superficie'][i])
                            ]
                        )
                        for i in range(len(df))
                    ]
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
