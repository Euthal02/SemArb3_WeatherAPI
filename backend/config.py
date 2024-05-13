from os import path as os_path
from os import environ as os_environ

basedir = os_path.abspath(os_path.dirname(__file__))

class Config:
    SECRET_KEY = os_environ.get('SECRET_KEY') or 'hallozusammen!4400'
    SQLALCHEMY_DATABASE_URI = os_environ.get('DATABASE_URI')\
        or 'sqlite:///' + os_path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DASHBOARD_ENABLED = os_environ.get('DASHBOARD_ENABLED') or False

