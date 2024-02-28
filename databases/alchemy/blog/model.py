from blog import db
from sqlalchemy.exc import IntegrityError


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @classmethod
    def add(cls, name, email):
        try:
            user = User(username=name, email=email)
            db.session.add(user)
            db.session.commit()
            return str(user)
        except IntegrityError as e:
            db.session.rollback()
            return e
