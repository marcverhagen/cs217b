from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fc3bb2a43ff1103895a4ee315ee27740'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_users.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return f'{User.query.all()}\n'

@app.route('/<string:name>')
def get_user(name):
    user = User.query.filter_by(username=name).first()
    return f'{user}\n'

@app.route('/<string:name>/<string:email>', methods=['POST'])
def add_user(name, email):
    user = User(username=name, email=email)
    db.session.add(user)
    db.session.commit()
    return f'{user}\n'


if __name__ == '__main__':
    app.run(debug=True)
