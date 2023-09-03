import requests
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import os



# Obtener los datos y crear el DataFrame
inflacion_anual = 'NY.GDP.DEFL.KD.ZG'
url = f'https://api.worldbank.org/v2/country/all/indicator/{inflacion_anual}?format=jsonstat'
response = requests.get(url)
json_data = response.json()

data = []
for i, value in enumerate(json_data["WDI"]["value"]):
    country_idx = i // (json_data["WDI"]["dimension"]["size"][1] * json_data["WDI"]["dimension"]["size"][2])
    series_idx = (i // json_data["WDI"]["dimension"]["size"][2]) % json_data["WDI"]["dimension"]["size"][1]
    year_idx = i % json_data["WDI"]["dimension"]["size"][2]

    country = list(json_data["WDI"]["dimension"]["country"]["category"]["label"].values())[country_idx]
    year = list(json_data["WDI"]["dimension"]["year"]["category"]["label"].values())[year_idx]

    data.append({"Country": country, "Year": year, "Inflation": value})

df_inflacion_anual = pd.DataFrame(data)

# Crear la aplicación Dash
app = dash.Dash(__name__)

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
    filtered_data = df_inflacion_anual[df_inflacion_anual['Country'] == selected_country]
    fig = px.line(filtered_data, x='Year', y='Inflation', title=f'Inflation in {selected_country}')
    return fig


if __name__ == '__main__':
    # Obtén el número de puerto proporcionado por Heroku o usa el puerto 8050 de forma predeterminada
    port = int(os.environ.get('PORT', 8050))
    
    # Ejecuta la aplicación en el puerto especificado
    app.run_server(host='0.0.0.0', port=port)

