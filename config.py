from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))

load_dotenv(path.join(basedir, '.env'))

SECRET_KEY = environ.get('SECRET_KEY')
PORT = '8001'
DEBUG = True
TESTING = True
FLASK_ENV = 'development'
ENV = 'development'

AWS_ACCESS_KEY_ID  = ''
AWS_SECRET_ACCESS_KEY  = ''
AWS_STORAGE_BUCKET_NAME  = ''