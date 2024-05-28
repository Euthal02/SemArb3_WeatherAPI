from app.weather import bp 
from backend.app.weather.weather_api import get_lat_and_lon_from_city_name, make_relay_api_call_based_on_lat_and_lon
from app.auth import token_auth
from app.models.weather import LocationIn, WeatherOut
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
    funny_forecast = raw_forecast_data

    # and finally return it.
    return funny_forecast