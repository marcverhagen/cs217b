# Flask examples

You need to install Flask and the Flask extension that supports building REST APIs.

```bash
$ pip install Flask
$ pip install Flask-RESTful
```

Suggested viewing for a simple introduction to Flask RESTful APIs:

[https://www.youtube.com/watch?v=s_ht4AKnWZg](https://www.youtube.com/watch?v=s_ht4AKnWZg)

The code for all examples below are in this repository under the path mentioned.


## Minimal example

This is the simplest Flask example and it is all you need to create a web server:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def howdy():
    return 'Howdy'

if __name__ == '__main__':
    app.run(debug=True)
```

This code is in [examples/minimal.py](examples/minimal.py), which has a few comments added. You run this by typing the following on the command line:

```bash
$ python minimal.py
```

This will give you some message which includes a note that the server is running at [http://127.0.0.1:5000](http://127.0.0.1:5000). You can access the service by pointing your browser at that webpage or by using `curl`:

```bash
$ curl http://127.0.0.1:5000
```

When you add the `-v` flag to curl you will notice that the content type return is text/html, which shows you that Flask's default is to serve a webpage and not the JSON that you would typically expect from a RESTful service.


## Returning JSON and adding POST requests

See [examples/minimal\_get_and\_post.py](examples/minimal_get_and_post.py) for commented code.

When you import `request` from the Flask package you have access to all goodies associated with the request. For example, you can (1) get the HTTP verb from the request and use it to determine what action to follow, and (2) retrieve the JSON that was associated with a POST request:

```python
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.get_json()
        return jsonify({'returning': user_input}), 418
    else:
        return jsonify('Howdy')
```

The 418 response code is optional, but if used will override the stard 200 response. This particular response is the "I'm a teapot" response and you can use it if you really do not want to do something with the request.

The only way to access this from a browser is to write some html that contains a form and then post the form data to the reqource we have here (using the submit button). Instead, we will do this with `curl`.

```bash
$ curl http://127.0.0.1:5000/ -H "Content-Type: application/json" -X POST -d '{"name": "sue"}'
```

This returns

```
{
  "returning": {
    "name": "sue"
  }
}
```

The `-H` option header sends an HTTP header, in this case stating that the attached content is JSON, not adding it may result in an error:

```bash
$ curl http://127.0.0.1:5000/ -X POST -d '{"name": "sue"}'
```

```html
<!doctype html>
<html lang=en>
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>Did not attempt to load JSON data because the request Content-Type was not 'application/json'.</p>
```

Recent versions of Flask have the `@app.get` and `@app.post` decorators, which makes for slightly cleaner code:

```python
@app.get('/')
def index_get():
    user_input = request.get_json()
    return jsonify({'returning': user_input}), 418

@app.post('/')
def index_post():
    return jsonify('Howdy')
```

You cannot use the same name for the two methods associated with the GET and POST request to the resource.

Finally, you can send any kind of data, not just JSON:

```python
@app.route('/bounce', methods=['POST'])
def bounce():
    answer = '\nContent-Type: %s\n\n' % request.headers['Content-Type']
    answer += str(request.data) + '\n\n'
    return answer
```


## Using the RESTful API

The above example mix a couple of things together, in particular, the location of the resource is closely associated with the function that does the work. Using the Flask RESTful API decouples these. This is shown in file [examples/minimal\_restful\_api.py](examples/minimal_restful_api.py).

```python
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Howdy(Resource):
    def get(self):
        return {'result': 'Howdy'}
    def post(self):
        some_json = request.get_json()
        return {'returning': some_json}, 201

class Multiply(Resource):
    def get(self, num):
        return { 'result': num * 10 }

api.add_resource(Howdy, '/')
api.add_resource(Multiply, '/multiply/<int:num>')

if __name__ == '__main__':
    app.run(debug=True)
```

Note how the resources themselves have no idea where they live, that is determined later, when they are added to the API.


## Rendering HTML

You can return an HTML string from the method that is attached to a resource, but that gets unwieldy quickly. It is better to use the `render_template()` method. See [examples/minimal\_render\_template.py](examples/minimal_render_template.py) for the main code, [templates/result.html](templates/result.html) for the Jinja template and [static/css/main.css](static/css/main.css) for the style sheet.

```python
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/multiply/<int:num>', methods=['POST'])
def multiply(num):
    some_json = request.get_json()
    result = num * some_json['number']
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
```

When you ping this with a number, you get the following (although in real life there would be some more whitespace in the result):

```bash
$ curl http://127.0.0.1:5000/multiply/5 -H "Content-Type: application/json" -d '{"number": 10}'
```

```html
<html>
  <head>
    <link rel="stylesheet" href="/static/css/main.css"/>
  </head>
  <body>
    <h2>Result</h2>
    <div>
      50
    </div>
  </body>
</html>
```

This is all by virtue of the `render_template()` method, which takes an Jinja template named `result.html` that is expected to live in the `templates` directory. Jinja is a mixture of HTML and some code that can be used to insert variables into the code. In this case we handed in a variable named `result` and the template checks for its existence before printing it:

```php
<html>
  <head>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}"/>
  </head>
  <body>
    <h2>Result</h2>
    {% if result %}
    <div>
      {{ result }}
    </div>
    {% endif %}
  </body>
</html>

```

Also note the style sheet, which is supposed to live in the static directory. In this case it is not doing anything because we ping the server from curl. The line `url_for('static', filename='css/main.css')` is boilerplate code and helps the server find the style sheet.

Not surpisingly, `render_template()` returns a string. You can also use the Flask Response class to return HTML string wrapped in a response object, which also let's you set headers:

```python
return Response(
    render_template('result.html', result='Howdy'),
    headers={'Content-Type': 'text/html'})
```