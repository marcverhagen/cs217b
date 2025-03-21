from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


users = {
    1: 'Wensleydale',
    2: 'Brie',
    3: 'Gouda' }


class Users(Resource):

    def get(self):
        return users


class User(Resource):

    def get(self, identifier: int):
        return users[identifier]

    def post(self, identifier: int):
        users[identifier] = request.form['cheese']


api.add_resource(Users, '/')
api.add_resource(User, '/<int:identifier>')


if __name__ == '__main__':

    app.run(debug=True)



"""

curl http://127.0.0.1:5000/

curl http://127.0.0.1:5000/1

curl http://127.0.0.1:5000/4 -X POST -d "cheese=Cheddar"

"""