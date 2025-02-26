from blog import app, db


@app.get('/')
def index():
    users = User.query.all()
    return f'{users}\n'
    bingo = Bingo()

@app.get('/<string:name>')
def get_user(name):
    user = User.query.filter_by(username=name).first()
    return f'{user}\n'

@app.post('/<string:name>/<string:email>')
def add_user(name, email):
    user = User(username=name, email=email)
    db.session.add(user)
    db.session.commit()
    return f'{user}\n'
