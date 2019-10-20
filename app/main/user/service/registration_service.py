import random, string
from datetime import datetime

from flask_api import status

from app.jobs.account_verification import send_async_email
from app.main.user.model.user import User
from app.main import redis, db


def __create_user(data):
    db.session.add(data)
    db.session.commit()

    return


def __check_verification_code(email, code):

    # check with redis
    return


def register_user(data):
    user = User.query.filter_by(email=data['email']).first()

    if not user:
        # set random code in email verification Queue
        verify_code = ''.join(random.sample(string.ascii_lowercase, 7))
        redis.set(data['email'], verify_code)
        email = {
            'subject': 'Asgard verification code',
            'body': 'verification code: ' + verify_code,
            'to': data['email']
        }
        send_async_email.delay(email)


    else:
        response = {
            "status": status.HTTP_409_CONFLICT,
            "message": "user already exists"
        }

        return response


def verify_user(data):

    user = User.query.filter_by(phonenumber=data['phonenumber']).first()

    if not user:

        new_user = User(
            firstname=data['firstname'],
            lastname=data['lastname'],
            password=data['password'],
            email=data['email'],
            role=data['role'],
            phonenumber=data['phonenumber'],
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow(),
            lastLogin=datetime.utcnow()

        )
        __create_user(new_user)

        return new_user.id
    else:
        return user.id
