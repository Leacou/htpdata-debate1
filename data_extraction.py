# data_extraction.py
import requests
import pandas as pd

def get_inflation_data(country):
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
    
    return df_inflacion_anual
