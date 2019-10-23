import json

from flask import request
from flask_restful import Resource, Api, reqparse
from flask_api import status

from app.main import app
from app.main.user.service.registration_service import verify_user, register_user
from app.main.user.service.user_service import user_info, delete_user, change_password, is_admin as check_permission
from app.main.user.service.authentication_service import get_userId
from app.main.user.model.user import UserSchema
from app.utils.authentication import has_authorized, encode_auth_token, decode_auth_token

api = Api(app)


class User(Resource):

    @has_authorized()
    def get(self, user_id):

        app.logger.info('call get user info with ID: %s' % user_id)

        try:
            user = user_info(user_id)
            user_schema = UserSchema()
            result = user_schema.dump(user)

            return json.dumps(result), status.HTTP_200_OK
        except Exception as e:
            app.logger.error(e)
            response = {
                'status': 'failed',
                'message': 'somthing wrong, please try again'
            }
            return response, status.HTTP_500_INTERNAL_SERVER_ERROR

    @has_authorized()
    def put(self, user_id):

        app.logger.info('call change password for user with ID: %s' % user_id)
        try:
            user = change_password(user_id, request.json['data'])
            if user:
                response = {
                    'message': 'user updated',
                    'status': 'success'
                }

                app.logger.info('password changed for user with ID: %s' % user_id)
                return response, status.HTTP_200_OK

            response = {
                'message': 'user not found',
                'status': 'failed'

            }

            return response, status.HTTP_409_CONFLICT
        except Exception as e:
            app.logger.error(e)
            response = {
                'message': 'something wrong, please try again',
                'status': 'failed'

            }

            return response, status.HTTP_500_INTERNAL_SERVER_ERROR

    @has_authorized()
    def delete(self, user_id):

        app.logger.info('call delete user API')

        auth_header = request.headers.get('Authorization')

        current_user = 0
        if auth_header:
            current_user = decode_auth_token(auth_header)

        is_admin = check_permission(current_user)
        if not is_admin:
            response = {
                'status': 'failed',
                'message': 'user has not permission'
            }
            return response, status.HTTP_403_FORBIDDEN

        try:
            delete_user(user_id)
            response = {
                'status': 'success',
                'message': 'user deleted with with user id %s' % user_id
            }
            app.logger.info('user deleted by adming: ' + current_user + 'user id: ' + user_id)
            return response, status.HTTP_200_OK

        except Exception as e:
            app.logger.error(e)
            response = {
                'status': 'failed',
                'message': 'something wrong, please try again'
            }
            return response, status.HTTP_500_INTERNAL_SERVER_ERROR


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
        app.logger.info('call user registeration API, requested user: ' + args['email'])
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
        app.logger.info('call verify account API for user: ' + args['email'])

        try:
            user_id = verify_user(args)

            if user_id == -1:
                response = {
                    'status': 'failed',
                    'message': 'try again'
                }
                return response, status.HTTP_400_BAD_REQUEST

            token = encode_auth_token(user_id)
            app.logger.info('verified user account, email: ' + args['email'])
            response = {
                'status': 'success',
                'token': token.decode()
            }
            return response, status.HTTP_200_OK
        except Exception as e:
            app.logger.error(e)
            response = {
                'status': 'failed',
                'message': 'something wrong, please try again'
            }
            return response, status.HTTP_400_BAD_REQUEST


class LoginUser(Resource):

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
        super().__init__()

    def post(self):

        args = self.reqparse.parse_args()
        app.logger.info('call login API, user: ' + args['email'])
        try:
            user = get_userId(args['email'], args['password'])
            if user is None:
                response = {
                    'status': 'failed',
                    'message': 'user does not exists'
                }
                return response, status.HTTP_404_NOT_FOUND
            token = encode_auth_token(user.id).decode()
            if token:
                response = {
                    'status': 'success',
                    'message': 'user logged in',
                    'token': token
                }
                app.logger.info('user logged in, email: ' + args['email'])
                return response, status.HTTP_200_OK

        except Exception as e:
            app.logger.error(e)
            response = {
                'status': 'failed',
                'message': 'something wrong, please try again',
            }
            return response, status.HTTP_500_INTERNAL_SERVER_ERROR


api.add_resource(RegisterUser, '/api/v1/user')
api.add_resource(VerifyUser, '/api/v1/verify')
api.add_resource(LoginUser, '/api/v1/token')
api.add_resource(User, '/api/v1/users/<int:user_id>')

