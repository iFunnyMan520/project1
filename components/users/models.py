import uuid
from sqlalchemy.sql import func

from settings import db


class User(db.Model):
    """
    Table contain all authorized users by their phone numbers
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String, unique=True)
    created_at = db.Column(db.DateTime, server_default=func.datetime())

    def __repr__(self):
        return f'({self.id}, {self.phone})'

    @staticmethod
    def get_by_phone(phone: str) -> 'User' or None:
        """
        Find registered user by phone number

        :param phone: user phone number
        :return: user model
        """
        return User.query.filter(User.phone == phone).first()

    @staticmethod
    def get_by_session(session_token: str):
        return User.query\
            .join(UserSessionToken)\
            .filter(UserSessionToken.session == session_token)\
            .first()

    @classmethod
    def login(cls, phone: str) -> 'UserConfirmationToken':
        """
        Start new authenticating process - delete current active sessions
        and create new confirmation token

        :param phone: user registration phone number
        :return: confirmation token
        """
        user = cls.get_by_phone(phone)

        if not user:
            # create user if not exists with same number
            user = User(phone=phone)
            db.session.add(user)
            db.session.commit()

        # find all active sessions and delete them
        UserSessionToken.query\
            .filter(UserSessionToken.user_id == user.id)\
            .delete()
        db.session.commit()

        # create new confirmation token
        new_token = UserConfirmationToken(
            user_id=user.id, token=str(uuid.uuid4()))
        db.session.add(new_token)
        db.session.commit()

        return new_token

    @classmethod
    def confirm_auth(cls, phone: str, confirmation_token: str) -> \
            ('UserSessionToken', 'User') or None:
        """
        Create new session token if combination from token and phone is ok

        :param phone: user phone number
        :param confirmation_token:
        :return: new session token or nothing
        """
        # find confirmation token
        user = cls.get_by_phone(phone)
        token_model = UserConfirmationToken.query\
            .filter(UserConfirmationToken.token == confirmation_token)\
            .filter(UserConfirmationToken.user_id == user.id)\
            .first()

        # return nothing if token does not exists
        if not token_model:
            return

        # and create new user session when token was found
        new_session = UserSessionToken(
            user_id=user.id,
            session=str(uuid.uuid4()))
        db.session.add(new_session)

        # delete confirmation token
        db.session.delete(token_model)
        db.session.commit()

        return new_session, user

    @property
    def serialized(self):
        return dict(id=self.id, phone=self.phone)


class UserConfirmationToken(db.Model):
    __tablename__ = 'users_token'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.ForeignKey('users.id'), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.datetime())


class UserSessionToken(db.Model):
    __tablename__ = 'users_session'

    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.String, unique=True)
    user_id = db.Column(db.ForeignKey('users.id'), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.datetime())
