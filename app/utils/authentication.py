import datetime
import jwt
from functools import wraps

from flask_restful import request
from flask_api import status

from app.main import app


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=600),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Validates the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def has_authorized():
    def _has_authorized(func):
        @wraps(func)
        def __has_authorized(*args, **kwargs):
            # just do here everything what you need

            auth_header = request.headers.get('Authorization')
            if auth_header != '':
                response = {
                    'message': 'Unauthorized user'
                }
                return response, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION

            result = func(*args, **kwargs)
            return result
        return __has_authorized
    return _has_authorized
