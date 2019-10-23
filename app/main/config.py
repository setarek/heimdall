import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY',
                           'sdkmf^&*(IJKNBVDSR%^YGVDSDR$^TGWEW$%FSCCDW#$%^&UHBvcdx@')

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    MAIL_DEFAULT_SENDER = 'serlina.karimi72@gmail.com'
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/heimdall_dev?user=setare&password=setare'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/heimdall_dev?user=setare&password=setare'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/heimdall?user=admin&password=admin'


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY