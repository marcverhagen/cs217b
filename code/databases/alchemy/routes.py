print('--- sources > __name__ = ', __name__)
print('--- sources > importing app and db')

from blog1a import app, db

print('--- sources > imported app', app)
print('--- sources > imported db', db)

@app.get('/')
def index():
    users = User.query.all()
    return f'{users}\n'

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

print('--- sources > defined routes')
