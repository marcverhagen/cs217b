"""

Totally simplistic web site which can multiply a number by 10.

Will improve on this in five ways:

1. It now has a very naive way of generating html. This works fine for trivial
   mini-pages, but it does not scale. Push the HTML into templates.
2. Hook up a style sheet to the template.
3. Create real multiplication and add addition.
4. Display the full equation in the result.
5. Use flask-restful.

"""

from flask import Flask, request

app = Flask(__name__)


@app.get('/')
def index():
    return ('<html>\n'
            '  <body>\n'
            '    <form action="/multiply" method="post">\n'
            '      <input type="text" name="number" />\n'
            '      <input type="submit" value="Submit">\n'
            '    </form>\n'
            '  </body>\n'
            '</html>\n')


@app.post('/multiply')
def multiply():
    num = request.form.get('number', type=int)
    if num is None:
        num = request.get_json()['number']
    result = num * 10
    return (
        '<html>\n'
        '  <body>\n'
        '    <h2>Result</h2>\n'
        f'    <div>{result}</div>\n'
        '    <p><a href="/">back</a></p>\n'
        '  </body>\n'
        '</html>\n')


if __name__ == '__main__':
    app.run(debug=True)


'''
curl http://127.0.0.1:5000/multiply -H "Content-Type: application/json" -d '{"number": 10}'
'''
