import os

import requests
from flask import Flask

from flaskr.cities import cities
from flaskr.reader_csv import code

# 'flask --app flaskr run' on root of the project to run

app = Flask(__name__)

@app.route("/<string:code>")
def weather(code):
    url = f"https://apiprevmet3.inmet.gov.br/previsao/{code}"

    try:
        response = requests.get(url)
        if response.status_code == 500:
            return {"error": "Someone Error ocurred in the Server"}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection Error"}

    try:
        response = response.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": "Error in the json build"}

    response = response[code]

    keys = []
    for key in response:
        keys.append(key)
    # Get the days in the first response

    week_weather = []
    for i in range(5):
        res = response[keys[i]]

        if i <= 1:
            list_weather = []

            for key in res:
                res = response[keys[i]]
                res = res.get(key)

                obj = {
                    "hour": key,
                    "temp_max": res.get("temp_max"),
                    "temp_min": res.get("temp_min"),
                    "umi_max": res.get("umidade_max"),
                    "umi_min": res.get("umidade_min"),
                    "day_week": res.get("dia_semana"),
                    "sunrise": res.get("nascer"),
                    "sunset": res.get("ocaso"),
                    "dir_air": res.get("dir_vento"),
                    "int_air": res.get("int_vento"),
                    "temp_max_goes_to": res.get("temp_max_tende"),
                    "temp_min_goes_to": res.get("temp_min_tende"),
                }

                list_weather.append(obj)

            week_weather.append(list_weather)
            res = response[keys[i]]

        else:
            # this else is just to other three days in the week

            obj = {
                "hour": key,
                "temp_max": res.get("temp_max"),
                "temp_min": res.get("temp_min"),
                "umi_max": res.get("umidade_max"),
                "umi_min": res.get("umidade_min"),
                "day_week": res.get("dia_semana"),
                "sunrise": res.get("nascer"),
                "sunset": res.get("ocaso"),
                "dir_air": res.get("dir_vento"),
                "int_air": res.get("int_vento"),
                "temp_max_goes_to": res.get("temp_max_tende"),
                "temp_min_goes_to": res.get("temp_min_tende"),
            }

            week_weather.append(obj)

    return {
        "code": code,
        "city": response[keys[3]].get("entidade"),
        "weather": week_weather,
    }

@app.route("/cities")
def city():
    return cities

@app.route("/cities/code/<string:city_name>")
def code_city(city_name):
    code_res = code(city_name)

    if code_res == "Not Found!":
        return {"err": "city not found"}

    return {"city": city_name, "code_city": code_res}

