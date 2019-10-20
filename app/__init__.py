from flask_restful import Api
from flask import Blueprint

from app.main.user.controller.user_controller import api as x

blueprint = Blueprint('api', __name__)

api = Api(blueprint)

api.resource(x, path='/user')