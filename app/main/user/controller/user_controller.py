from flask import jsonify, request
from flask_restful import Resource, Api, reqparse, marshal
from flask_api import status

import json

from app.main import app
from app.main.user.service.registration_service import verify_user, register_user
from app.main.user.service.user_service import user_info, delete_user, change_password
from app.main.user.model.user import User, UserSchema

api = Api(app)
parser = reqparse.RequestParser()

class User(Resource):

    def get (self, user_id):

        user = user_info(user_id)
        user_schema = UserSchema()
        result = user_schema.dump(user)

        return json.dumps(result)

    def delete(self, user_id):

        user = delete_user(user_id)
        user_schema = UserSchema()
        return user_schema.dump(user)

    def put(self, user_id):

        user = change_password(user_id, request.json['data'])
        if user:
            response = {
                'message': 'user updated',
                'status': 'success'
            }
            return response, status.HTTP_200_OK

        response = {
            'message': 'user not found',
            'status': 'fail'

        }

        return response, status.HTTP_409_CONFLICT




api.add_resource(User, '/api/v1/user/<int:user_id>')
