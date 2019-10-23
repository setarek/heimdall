from datetime import datetime

from app.main import db
from app.main.user.model.user import User
from app.utils.authentication import encode_auth_token, decode_auth_token
from app.test.base import BaseTestCase

class TestUserToken(BaseTestCase):
    test_user = None # <--- 👈

    def setUp(self):
        db.create_all()
        db.session.commit()

        user = User(
            phonenumber='01234567890',
            email='test@test.com',
            firstname='bruce',
            lastname='banner',
            role=1,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow(),
            lastLogin=datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
        self.test_user = user.id
    def test_user_token(self):

        auth_token = encode_auth_token(self.test_user)

        decoded_user = decode_auth_token(auth_token.decode())
        self.assertTrue(decoded_user == self.test_user)