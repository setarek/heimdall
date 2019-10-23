import os
import redis
import logging
from logging.handlers import RotatingFileHandler

from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url("redis://localhost:6379")
app = Flask(__name__)

marshmallow = Marshmallow(app)
celery = Celery(__name__, broker='redis://localhost:6379/0')

def create_app(config_name):

    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    celery.conf.update(app.config)


    # celery config
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    app.config['BROKER_TRANSPORT'] = 'redis'

    # mail config
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = "serlina.karimi72@gmail.com"
    app.config['MAIL_PASSWORD'] = "seka7296AI"
    app.config['MAIL_DEFAULT_SENDER'] = "serlina.karimi72@gmail.com"

    # Logger config
    handler = RotatingFileHandler('heimdal.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    return app
