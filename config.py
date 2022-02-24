"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv
import os


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = environ.get('SECRET_KEY')
MONGO_URI = os.getenv('MONGO_URI')
