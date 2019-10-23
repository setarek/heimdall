import datetime

from app.main import marshmallow

from app.main import db, flask_bcrypt

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.INTEGER, primary_key=True)
    phonenumber = db.Column(db.String(100))
    email = db.Column(db.String(100))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    role = db.Column(db.Integer, default=1)
    password = db.Column(db.String(1000))
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    lastLogin = db.Column(db.DateTime)


class UserSchema(marshmallow.ModelSchema):
    class Meta:
        model = User
