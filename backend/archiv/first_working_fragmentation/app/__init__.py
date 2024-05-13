#!/usr/bin/python3
from apiflask import APIFlask
from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = APIFlask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    from app.students import bp as routes_bp
    from app.courses import bp as courses_bp
    app.register_blueprint(routes_bp, url_prefix='/students')
    app.register_blueprint(courses_bp, url_prefix='/courses')

    # Datenbanktabellen anlegen
    with app.app_context():
        db.create_all()

    @app.get('/')
    def absolute_root_path():
        return {'message': 'This is the root directory of my Flask Server. Try GET /student'}

    return app