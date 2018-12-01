from commandment.models import db
from authlib.flask.oauth2.sqla import OAuth2ClientMixin

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    display_name = db.Column(db.String)
    password = db.Column(db.String)

    def get_user_id(self):
        return self.id


class Client(db.Model, OAuth2ClientMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')

