from apiflask import Schema
from apiflask.fields import String, Integer
from apiflask.validators import Length, Email

class LocationIn(Schema):
    city_name = String(required=True, validate=Length(0, 128))
    country_code = String(required=True, validate=Length(0, 3))

# define the schema for the user input
class WeatherIn(Schema):
    name = String(required=True, validate=Length(0, 128))
    email = String(required=True, validate=[Length(0, 128), Email()])
    password = String(required=True, validate=Length(0, 256))

# define the schema for the output
class WeatherOut(Schema):
    id = Integer()
    name = String()
    email = String()
    password = String()