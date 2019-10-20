from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
import redis
import os
from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url("redis://localhost:6379")
app = Flask(__name__)

marshmallow = Marshmallow(app)


def create_app(config_name):

    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app