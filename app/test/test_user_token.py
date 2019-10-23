from datetime import datetime

from app.main import db
from app.main.user.model.user import User
from app.utils.authentication import encode_auth_token, decode_auth_token
from app.test.base import BaseTestCase, test_user

class TestUserToken(BaseTestCase):

    def test_user_token(self):

        auth_token = encode_auth_token(test_user)

        decoded_user = decode_auth_token(auth_token.decode())
        self.assertTrue(decoded_user == test_user)

