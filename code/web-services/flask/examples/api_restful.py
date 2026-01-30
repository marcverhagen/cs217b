from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Howdy(Resource):

    def get(self):
        return {'result': 'Howdy'} 

    def post(self):
        some_json = request.get_json()
        return {'returning': some_json}, 200


class Multiply(Resource):

    def get(self, num):
        return { 'result': num * 10 }


api.add_resource(Howdy, '/')
api.add_resource(Multiply, '/multiply/<int:num>')


if __name__ == '__main__':
    app.run(debug=True)


'''

curl http://127.0.0.1:5000/

curl http://127.0.0.1:5000/ -H "Content-Type: application/json" -d '{"name": "sue"}'

curl http://127.0.0.1:5000/multiply/23

'''
