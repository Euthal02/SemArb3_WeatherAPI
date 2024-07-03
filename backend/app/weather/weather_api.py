#############################################
#  Based on:                               ##
#  https://openweathermap.org/forecast5    ##
#############################################
from requests import get as requests_get
from apiflask import abort as flask_abort
from flask import current_app

RELAY_API_URL = "http://api.openweathermap.org"
FORECAST_LENGTH = 10  # in 3 hour chunks


def get_city_name_from_lat_and_lon(lattitude, longitude):
    response = requests_get(f"{RELAY_API_URL}/geo/1.0/reverse?lat={lattitude}&lon={longitude}&limit=1&appid={current_app.config['WEATHER_API_KEY']}")
    if response.json():
        city_name = response.json()[0]["name"]
        country = response.json()[0]["country"]
        return city_name, country
    else:
        flask_abort(404, "This city could not be found!")


def make_relay_api_call_based_on_lat_and_lon(lattitude, longitude):
    response = requests_get(f"{RELAY_API_URL}/data/2.5/forecast?lat={lattitude}&lon={longitude}&units=metric&cnt={FORECAST_LENGTH}&appid={current_app.config['WEATHER_API_KEY']}")
    response_as_json = response.json()
    return response_as_json
