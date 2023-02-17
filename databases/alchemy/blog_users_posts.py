from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fc3bb2a43ff1103895a4ee315ee27740'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_users_posts.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}' posts={self.posts})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.content}')"


if __name__ == '__main__':
    app.run(debug=True)


"""

The code below works from Python unless you already have a user with
username=sue and email=sue@example.com

from blog_users_posts import db, User, Post
db.create_all()

sue = User(username='sue', email="sue@example.com")
db.session.add(sue)
db.session.commit()

post1 = Post(title="p1", content="stuff1", user_id=sue.id)
post2 = Post(title="p2", content="stuff2", user_id=sue.id)
db.session.add_all([post1, post2])
db.session.commit()

"""
