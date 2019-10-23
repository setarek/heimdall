from datetime import datetime

from app.main import db
from app.main.user.model.user import User
from app.utils.authentication import encode_auth_token
from app.test.base import BaseTestCase

class TestUserAuthentication(BaseTestCase):

    def test_user_auth(self):

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

        auth_token = encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))