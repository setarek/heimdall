import json

from flask import request
from flask_restful import Resource, Api, reqparse
from flask_api import status

from app.main import app
from app.main.user.service.registration_service import verify_user, register_user
from app.main.user.service.user_service import user_info, delete_user, change_password
from app.main.user.model.user import UserSchema
from app.utils import authentication

api = Api(app)
parser = reqparse.RequestParser()


class User(Resource):

    def get(self, user_id):

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


class RegisterUser(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required=True,
            help='no email provided',
            location=['form', 'json']
        )

    def post(self):

        args = self.reqparse.parse_args()
        return register_user(args)


class VerifyUser(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required=True,
            help='no email provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'password',
            required=True,
            help='no password provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'phonenumber',
            required=True,
            help='no phonenumber provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'verification_code',
            required=True,
            help='no verification code provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'firstname',
            required=True,
            help='no firstname provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'lastname',
            required=True,
            help='no lastname provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'role',
            required=False,
            location=['form', 'json']
        )

        super().__init__()

    def post(self):

        args = self.reqparse.parse_args()

        # TODO: Check Verification code match or not

        try:
            user_id = verify_user(args)

            if user_id == -1:
                response = {
                    'status': 'failed',
                    'message': 'try again'
                }
                return response, status.HTTP_400_BAD_REQUEST

            token = authentication.encode_auth_token(user_id)
            response = {
                'status': 'success',
                'token': token.decode()
            }
            return response, status.HTTP_200_OK
        except Exception as e:
            response = {
                'status': 'failed',
                'message': e
            }
            return response, status.HTTP_400_BAD_REQUEST


api.add_resource(RegisterUser, '/api/v1/register')
api.add_resource(VerifyUser, '/api/v1/verify')


api.add_resource(User, '/api/v1/user/<int:user_id>')
