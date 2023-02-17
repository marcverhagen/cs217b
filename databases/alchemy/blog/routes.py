from blog import app
from blog.model import User


@app.route('/')
def select_all():
    return '\n'.join([f'{row}' for row in User.query.all()]) + '\n'

@app.route('/<string:name>')
def select(name):
    user = User.query.filter_by(username=name).first()
    return f'{user}\n'

@app.route('/<string:name>/<string:email>', methods=['POST'])
def insert(name, email):
    result = User.add(name, email)
    return f'{result}\n'
