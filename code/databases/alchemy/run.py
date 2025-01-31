from blog import app, db


if __name__ == '__main__':

    with app.app_context():
        db.create_all()
    app.run(debug=True)


'''

curl 127.0.0.1:5000
curl 127.0.0.1:5000/admin
curl 127.0.0.1:5000/admin/admin@example.com -X POST
curl 127.0.0.1:5000/guest/guest@example.com -X POST

'''