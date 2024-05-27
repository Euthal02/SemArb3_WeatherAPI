from apiflask import APIBlueprint

bp = APIBlueprint('weather', __name__)

from app.weather import routes