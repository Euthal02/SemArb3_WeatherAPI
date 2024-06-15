#!/usr/bin/python3
from apiflask import APIFlask
from config import Config
from app.extensions import db
from flask_cors import CORS
import flask_monitoringdashboard as dashboard


def create_app(config_class=Config, config_overwrites=dict()):
    app = APIFlask(__name__)
    CORS(app, send_wildcard=True)
    app.config.from_object(config_class)

    # this is necessary for the test env to start up correctly.
    if config_overwrites:
        app.config.update(config_overwrites)

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from app.weather import bp as weather_bp
    app.register_blueprint(weather_bp, url_prefix='/weather')

    # Datenbanktabellen anlegen
    with app.app_context():
        db.create_all()

    @app.get('/')
    def absolute_root_path():
        return {'message': 'Welcome to our Weather App!'}

    if app.config['DASHBOARD_ENABLED']:
        dashboard.config.init_from(file='monitoring_dashboard_config.cfg')
        dashboard.bind(app)

    return app
