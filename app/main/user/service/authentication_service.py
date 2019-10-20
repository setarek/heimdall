from app.main.user.model.user import User
from app.main import db


def get_userId(email, password):

    user = User.query.filter_by(email=email, password=password).first()
    return user.id



