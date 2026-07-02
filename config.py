import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')


class DevelopmentConfig(Config):
    DEBUG=True


class ProductionConfig(Config):
    DEBUG=False


