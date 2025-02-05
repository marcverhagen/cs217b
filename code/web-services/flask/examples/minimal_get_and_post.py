from flask import Flask, jsonify, request

app = Flask(__name__)

# curl http://127.0.0.1:5000
# curl http://127.0.0.1:5000/ -v -H "Content-Type: application/json" -d '{"name": "sue"}'
# Note the methods argument, the default is a list with just GET, if you do not
# add POST then the resource will not accept POST requests.
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return jsonify('Howdy')
    else:
        user_input = request.get_json()
        # Using jsonify to create proper JSON, but you could just return the
        # dictionary object that you got from get_json(). The optional second
        # parameter will override the standard 200 response.
        return jsonify({'returning': user_input}), 418

# Instead of @app.route you can use @app.get and @app.post

# curl http://127.0.0.1:5000/help
@app.get('/help')
def help():
    return "<p>Getting extremely minimal help via a GET request</p>"

# curl --request POST http://127.0.0.1:5000/help
@app.post('/help')
def help_post():
    return "<p>Getting extremely minimal help via a POST request</p>"

# curl http://127.0.0.1:5000/multiply/5
# This uses a typed subpath of multiply, in effect creating an unlimited amount
# of resources.
@app.route('/multiply/<int:num>')
def multiply(num):
    return jsonify({'result': num * 10})

# curl http://127.0.0.1:5000/multiply2?num=5
# A variant of the above, where you only have one resource, but you hand it a
# query parameter.
@app.route('/multiply2')
def multiply2():
    num = request.args.get('num')
    return jsonify({'result1': num * 10})

# curl http://127.0.0.1:5000/multiply3?num=5
# A variant of the above, where you only have one resource, but you hand it a
# query parameter.
@app.route('/multiply3')
def multiply3():
    num = request.args.get('num', type=int)
    return jsonify({'result1': num * 10})

# curl http://127.0.0.1:5000/multiply4 -H "Content-Type: application/json" -d '{"number": 5}'
# You can also hand in the number via the POST attachment.
@app.route('/multiply4', methods=['POST'])
def multiply4():
    some_json = request.get_json()
    return jsonify({'result': some_json['number'] * 10})

# curl http://127.0.0.1:5000/bounce -H "Content-Type: text/plain" -d 'Number 5'
# curl http://127.0.0.1:5000/bounce -H "Content-Type: application/json" -d '{"Number": 5}'
# The request object also gives access to the raw data of the POST request
@app.route('/bounce', methods=['POST'])
def bounce():
    r = request
    answer = (
        f'{r.method} {r.path} {r.environ.get("SERVER_PROTOCOL")}\n'
        + f'{r.headers}{r.json}\n')
    return answer


if __name__ == '__main__':
    app.run(debug=True)


'''

Two ways of sending the content of the POST request:

$ curl http://127.0.0.1:5000/ -H "Content-Type: application/json" -X POST -d '{"name": "sue"}'
$ curl http://127.0.0.1:5000/ -H "Content-Type: application/json" -X POST -d @input/message.json

When you use -d the POST method is implied so you can shorten this a bit:

$ curl http://127.0.0.1:5000/ -H "Content-Type: application/json" -d '{"name": "sue"}'
$ curl http://127.0.0.1:5000/ -H "Content-Type: application/json" -d @input/message.json

We can send something that is not JSON:

$ curl http://127.0.0.1:5000/bounce -H "Content-Type: application/json" -d @input/message.json
$ curl http://127.0.0.1:5000/bounce -H "Content-Type: text/plain" -d @input/message.txt
$ curl http://127.0.0.1:5000/bounce -H "Content-Type: text/xml" -d @input/message.xml

'''
