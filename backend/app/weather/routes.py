from app.weather import bp 
from app.weather.weather_api import get_city_name_from_lat_and_lon, make_relay_api_call_based_on_lat_and_lon
from app.weather.llm_api import send_message_to_llm
from app.auth import token_auth
from app.models.weather import LocationIn, WeatherOut
from json import dumps as json_dumps
from apiflask import abort as flask_abort
#import logging


# get weather info
@bp.get('/lookup')
@bp.auth_required(token_auth)
@bp.input(LocationIn, location='query')
@bp.output(WeatherOut)
def weather_data_from_lattitude_and_longitude(query_data):
    # first, get the forecast data
    lattitude = query_data['lattitude']
    longitude = query_data['longitude']
    if lattitude == 0 or longitude == 0:
        flask_abort(404, f"On this geolocation is no city: {lattitude}, {longitude}")
    city_name, country = get_city_name_from_lat_and_lon(lattitude, longitude)
    raw_forecast_data = make_relay_api_call_based_on_lat_and_lon(lattitude, longitude)

    # second, we have to create a funny forecast from it.
    forecast_as_string = json_dumps(raw_forecast_data)
    funny_forecast = send_message_to_llm(forecast_as_string)

    # and finally return it.
    return {"city_name": city_name, "country_code": country, "message": funny_forecast}
