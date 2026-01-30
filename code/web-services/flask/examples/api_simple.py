from flask import Flask, request

app = Flask(__name__)


@app.get("/")
def get_string():
    return {'result': 'Howdy'} 


@app.post("/")
def bounce_string():
    some_json = request.get_json()
    return {'returning': some_json}, 200


@app.get('/multiply/<int:num>')
def multiply(num):
    return { 'result': num * 10 }


if __name__ == '__main__':
    app.run(debug=True)


'''

curl http://127.0.0.1:5000/

curl http://127.0.0.1:5000/ -H "Content-Type: application/json" -d '{"name": "sue"}'

curl http://127.0.0.1:5000/multiply/23

'''
