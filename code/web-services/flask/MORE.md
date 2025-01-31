## Rendering HTML

You can return an HTML string from the method that is attached to a resource, but that gets unwieldy quickly. It is better to use the `render_template()` method. See `web-services/flask/examples/minimal_render_template.py` for the code.

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


```

Returning HTML:
    return '<html>Howdy</html>'
    return render_template('result.html', result='Howdy')
    return Response(render_template('result.html', result='Howdy'),
                    headers={'Content-Type': 'text/html'})

importing model
```