from apiflask import APIBlueprint

bp = APIBlueprint('user', __name__)

from app.users import routes