from datetime import datetime
from flask_testing import TestCase

from app.main import db
from app.main import app
from app.main.user.model.user import User

test_user = 0
class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

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
        test_user = user.id
    def tearDown(self):
        db.session.remove()
        db.drop_all()
