from app.main import db


def add_token_blacklist(token):

    db.session.add(token)
    db.session.commit()
    return