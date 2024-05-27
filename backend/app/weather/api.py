#############################################
##  Based on:                              ##
##  https://openweathermap.org/forecast5   ##
#############################################
from requests import get as requests_get

RELAY_API_URL = "http://api.openweathermap.org"
RELAY_API_KEY = "ea0c217526b140ece2689be7d00653bb"

def get_lat_and_lon_from_city_name(city_name, country=None):
    response = requests_get(f"{RELAY_API_URL}/geo/1.0/direct?q={city_name},{country}&limit=1&appid={RELAY_API_KEY}")
    return_lat = response.json()[0]["lat"]
    return_lon = response.json()[0]["lon"]
    return return_lat, return_lon

def make_relay_api_call_based_on_lat_and_lon(lattitude, longitude):
    response = requests_get(f"{RELAY_API_URL}/data/2.5/forecast?lat={lattitude}&lon={longitude}&units=metric&cnt=6&appid={RELAY_API_KEY}")
    response_as_json = response.json()
    return(response_as_json)
