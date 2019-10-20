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

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.email)


class UserSchema(marshmallow.ModelSchema):
    class Meta:
        model = User
