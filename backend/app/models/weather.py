from apiflask import Schema
from apiflask.fields import String
from apiflask.validators import Length


class LocationIn(Schema):
    lattitude = String(required=True, validate=Length(0, 128))
    longitude = String(required=True, validate=Length(0, 128))


# define the schema for the output
class WeatherOut(Schema):
    city_name = String(required=True, validate=Length(0, 128))
    country_code = String(required=True, validate=Length(0, 3))
    message = String(required=True)
