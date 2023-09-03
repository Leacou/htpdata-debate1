import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import os
import data_extraction  # Importa el módulo de extracción de datos
import visualizations  # Importa el módulo de visualizaciones

app = dash.Dash(__name__)

# Obtener los datos de inflación utilizando la función del módulo data_extraction
df_inflacion_anual = data_extraction.get_inflation_data('Argentina')

app.layout = html.Div([
    dcc.Graph(id='inflation-graph'),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df_inflacion_anual['Country'].unique()],
        value='USA',
        multi=False,
        searchable=True
    )
])

@app.callback(
    Output('inflation-graph', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_graph(selected_country):
    # Utiliza la función del módulo visualizations para crear la visualización
    fig = visualizations.create_inflation_chart(df_inflacion_anual, selected_country)
    return fig


if __name__ == '__main__':
    # Obtén el número de puerto proporcionado por Heroku o usa el puerto 8050 de forma predeterminada
    port = int(os.environ.get('PORT', 8050))
    
    # Ejecuta la aplicación en el puerto especificado
    app.run_server(host='0.0.0.0', port=port)

