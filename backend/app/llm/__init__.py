from apiflask import APIBlueprint

bp = APIBlueprint('llm', __name__)

from app.llm import routes