"""

Not working, needs to be fixed.

"""


from blog1 import User, app, db

print(f'\napp = {app}\ndb  = {db}\n')

admin = User(username='admin', email='admin@example.com')
guest = User(username='guest', email='guest@example.com')

admin.id, admin.username, admin.email

print(admin)


with app.app_context():
    db.create_all()
    #db.session.add(admin)
    #db.session.commit()
    print('0', User.query.all())


with app.app_context():
	print('1', User.query.all())
    #print(User.query.filter_by(username='admin').first())
    #print(User.query.filter_by(username='guest').first())

with app.app_context():
    db.session.add(guest)
    print('2', User.query.all())


with app.app_context():
    db.session.add(guest)
    db.session.commit()
    print('3', User.query.all())

with app.app_context():
    #db.session.add(admin)
    #db.session.commit()
    print('4', User.query.all())
