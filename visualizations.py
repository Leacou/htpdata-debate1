# visualizations.py
import plotly.express as px

def create_inflation_chart(data, country):
    filtered_data = data[data['Country'] == country]
    fig = px.line(filtered_data, x='Year', y='Inflation', title=f'Inflation in {country}')
    return fig
