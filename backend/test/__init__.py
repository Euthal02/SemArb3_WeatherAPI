from pytest import fixture as pytest_fixture
from os import path as os_path
from app import create_app
from test.create_test_data import create_test_data

basedir = os_path.abspath(os_path.dirname(__file__))


@pytest_fixture
def client():

    overwrite_config = {
        "TESTING": True,
        "SECRET_KEY": 'hallozusammen!4400',
        "SQLALCHEMY_DATABASE_URI": 'sqlite:///' + os_path.join(basedir, 'app.db'),
        "DASHBOARD_ENABLED": False
    }
    app = create_app(config_overwrites=overwrite_config)

    with app.app_context():
        create_test_data()

    return app.test_client()
