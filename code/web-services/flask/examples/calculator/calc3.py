"""

Simple calculator web site.

- ✔︎ Moves HTML into templates.
- ✔︎ Uses stylesheet.
- Adds multiplication of two numbers and adds addition.
- Display the two inputs in the result.
- Uses flask-restful.

"""

from flask import Flask, request, render_template

app = Flask(__name__)


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/multiply')
def multiply():
    num = request.form.get('number', type=int)
    if num is None:
        num = request.get_json()['number']
    result = num * 10
    return render_template('result2.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)


'''
curl http://127.0.0.1:5000/multiply -H "Content-Type: application/json" -d '{"number": 10}'
'''
