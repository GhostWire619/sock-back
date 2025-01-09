from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config("SECRET_KEY", default="supersecretkey")
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', default=False, cast=bool)

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, 'dev.db')
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://avnadmin:AVNS_wAH0cl_M1NH9lLTNimf@myapp-db-lugata619-7bcd.g.aivencloud.com:26008/defaultdb?sslmode=require"
    #SQLALCHEMY_DATABASE_URI = config("SQLALCHEMY_DATABASE_URI")
    DEBUG = config('DEBUG', default=False, cast=bool)
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', default=False, cast=bool)
    SQLALCHEMY_ECHO = config('ECHO', default=False, cast=bool)

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, 'test.db')
    DEBUG = True
    SQLALCHEMY_ECHO = False
