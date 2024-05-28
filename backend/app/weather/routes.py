from app.weather import bp 
from app.weather.weather_api import get_lat_and_lon_from_city_name, make_relay_api_call_based_on_lat_and_lon
from app.weather.llm_api import send_message_to_llm
from app.auth import token_auth
from app.models.weather import LocationIn, WeatherOut
from json import dumps as json_dumps
#import logging

# get weather info
@bp.get('/lookup')
@bp.auth_required(token_auth)
@bp.input(LocationIn, location='query')
#@bp.output(WeatherOut)
def weather_data_from_cityname_and_countrycode(query_data):
    # first, get the forecast data
    city_name = query_data['city_name']
    country_code = query_data['country_code']
    lattitude, longitude = get_lat_and_lon_from_city_name(city_name, country_code)
    raw_forecast_data = make_relay_api_call_based_on_lat_and_lon(lattitude, longitude)

    # second, we have to create a funny forecast from it.
    # ToDo: create funny forecast
    forecast_as_string = json_dumps(raw_forecast_data)
    funny_forecast = send_message_to_llm(forecast_as_string)

    # and finally return it.
    return funny_forecast