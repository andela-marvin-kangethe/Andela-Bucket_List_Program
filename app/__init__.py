from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import *

db = SQLAlchemy()

def create_app(config_name):
    """
    This function creates a Flask instance for
    the application and configures it.
    """
    application = Flask(__name__)

    application.config.from_object(config[config_name])

    db.init_app(application)

    return application


app = create_app('development')


