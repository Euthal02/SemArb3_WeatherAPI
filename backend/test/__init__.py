from pytest import fixture as pytest_fixture
from os import path as os_path
from os import environ as os_environ
from app import create_app
from test.create_test_data import create_test_data

basedir = os_path.abspath(os_path.dirname(__file__))


@pytest_fixture
def client():

    overwrite_config = {
        "TESTING": True,
        "SECRET_KEY": 'hallozusammen!4400',
        "SQLALCHEMY_DATABASE_URI": 'sqlite:///' + os_path.join(basedir, 'app.db'),
        "DASHBOARD_ENABLED": False,
        "ORGANIZATION": os_environ.get('ORGANIZATION'),
        "PROJECT": os_environ.get('PROJECT'),
        "API_KEY": os_environ.get('API_KEY'),
        "ASSISTANT_ID": os_environ.get('ASSISTANT_ID'),
        "WEATHER_API_KEY": os_environ.get('WEATHER_API_KEY')
    }
    app = create_app(config_overwrites=overwrite_config)

    with app.app_context():
        create_test_data()

    return app.test_client()
