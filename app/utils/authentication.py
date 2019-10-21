import datetime
import jwt
from functools import wraps

from flask_restful import request
from flask_api import status

from app.main import app
from app.main.user.model.black_list import BlacklistToken


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
        is_blacklisted_token = check_blacklist(auth_token)
        if is_blacklisted_token:
            return 'Token blacklisted. Please log in again.'
        else:
            return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def check_blacklist(auth_token):
    # check whether auth token has been blacklisted
    res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
    if res:
        return True
    else:
        return False


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
