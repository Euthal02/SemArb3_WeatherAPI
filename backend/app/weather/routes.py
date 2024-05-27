from app.weather import bp 
#from app.extensions import db
#from werkzeug.security import generate_password_hash
from apiflask import abort as flask_abort
#import logging
from app.weather.api import get_lat_and_lon_from_city_name, make_relay_api_call_based_on_lat_and_lon
from app.auth import token_auth
from app.models.weather import LocationIn, WeatherIn, WeatherOut

# get weather info
@bp.get('/lookup')
@bp.auth_required(token_auth)
@bp.input(LocationIn, location='query')
#@bp.output(WeatherOut)
def weather_data_from_cityname_and_countrycode(query_data):
    city_name = query_data['city_name']
    country_code = query_data['country_code']
    lattitude, longitude = get_lat_and_lon_from_city_name(city_name, country_code)
    return make_relay_api_call_based_on_lat_and_lon(lattitude, longitude)