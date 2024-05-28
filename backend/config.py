from os import path as os_path
from os import environ as os_environ

basedir = os_path.abspath(os_path.dirname(__file__))

class Config:
    # env variables
    SECRET_KEY = os_environ.get('SECRET_KEY')
    DASHBOARD_ENABLED = os_environ.get('DASHBOARD_ENABLED')
    SQLALCHEMY_DATABASE_URI = os_environ.get('DATABASE_URI')
    ORGANIZATION = os_environ.get('ORGANIZATION')
    PROJECT = os_environ.get('PROJECT')
    API_KEY = os_environ.get('API_KEY')
    ASSISTANT_ID = os_environ.get('ASSISTANT_ID')

    # control variables
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
