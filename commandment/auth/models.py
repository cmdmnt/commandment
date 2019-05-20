from commandment.models import db
from authlib.flask.oauth2.sqla import OAuth2ClientMixin, OAuth2TokenMixin


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    fullname = db.Column(db.String)
    password = db.Column(db.String)

    def get_user_id(self):
        """This method is implemented as part of the Resource Owner interface for Authlib."""
        return self.id


class Client(db.Model, OAuth2ClientMixin):
    """OAuth 2 Client"""
    __tablename__ = 'oauth2_clients'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')
    )
    user = db.relationship('User')


class Token(db.Model, OAuth2TokenMixin):
    """Bearer Token"""
    __tablename__ = 'oauth2_tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')
    )
    user = db.relationship('User')

