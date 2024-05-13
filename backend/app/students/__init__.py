from apiflask import APIBlueprint

bp = APIBlueprint('student', __name__)

from app.students import routes