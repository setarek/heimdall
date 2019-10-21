from app.main.user.model.user import User
from app.main import db


def user_info(user_id):
    """
    Get user information by user id
    :param user_id: user_id
    :return: user object
    """
    return User.query.filter_by(id=user_id).first()


def delete_user(user_id):

    """
    Delte user by user id
    :param user_id:
    :return:
    """

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return



def change_password(user_id, data):
    """
    :param user_id:  user id
    :param new_password: new password requested user
    :return: user object
    """

    try:

        # TODO: do not forget hash password
        is_equal = __compare_password(data['new_password'],
                                      data['confirm_password'])
        if is_equal:
            user = User.query.filter_by(id=user_id).first()
            if user:

                if data['old_password'] != user['password']:
                    return
                user.update(dict(password=data['new_password']))
                db.session.commit()
                return user
        return
    except Exception as e:
        raise e


def is_admin(user_id):

    """
    :param user_id:
    :return: return true if user is admin
    """
    user = User.query.get(user_id)
    if user.role == 2:
        return True
    return False


def __compare_password(old_password, confirm_passwod):

    if old_password == confirm_passwod:
        return True
    return False
