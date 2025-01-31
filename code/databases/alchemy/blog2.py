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
        return f"User(id={self.id} name={self.username} email={self.email} posts={self.posts})"

    def pp(self):
        posts = '\n    '.join([str(p) for p in self.posts])
        return f"User(id={self.id} name={self.username} email={self.email})\n    {posts})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post(title={self.title} content='{self.content}')"


@app.get('/')
def index():
    users = User.query.all()
    return f'{users}\n'

@app.get('/<string:name>')
def get_user(name):
    user = User.query.filter_by(username=name).first()
    return f'{user.pp()}\n'

@app.post('/<string:name>/<string:email>')
def add_user(name, email):
    user = User(username=name, email=email)
    db.session.add(user)
    db.session.commit()
    return f'{user}\n'

@app.post('/<string:name>/<string:post_title>/<string:post_content>')
def add_post(name, post_title, post_content):
    user = User.query.filter_by(username=name).first()
    post = Post(title=post_title, content=post_content, user_id=user.id)
    print('>>>', post.author)
    db.session.add(post)
    print('>>>', post.author)
    db.session.commit()
    print('>>>', post.author)
    return f'{user.pp()}\n'


if __name__ == '__main__':

    with app.app_context():
        db.create_all()
    app.run(debug=True)


"""

curl http://127.0.0.1:5000/
curl http://127.0.0.1:5000/john
curl -X POST http://127.0.0.1:5000/john/john@example.com
curl -X POST http://127.0.0.1:5000/john/hello/world
curl -X POST http://127.0.0.1:5000/john/byebye/country

"""
