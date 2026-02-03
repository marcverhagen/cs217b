"""

Simple calculator web site.

- ✔︎ Moves HTML into templates.
- ✔︎ Uses stylesheet.
- ✔︎ Adds multiplication of two numbers and adds addition.
- ✔︎ Display the two inputs in the result.
- ✔︎ Uses flask-restful.

"""

from flask import Flask, request, render_template, Response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Home(Resource):

    def get(self):
        return Response(render_template('index2.html'), mimetype='text/html')


class CalculatorResult(Resource):

    def post(self):
        if request.form:
            x = request.form.get('x', type=int)
            y = request.form.get('y', type=int)
            op = request.form.get('operator', type=str)
        else:
            parameters = request.get_json()
            x = parameters['x']
            y = parameters['y']
            op = parameters['operator']
        result = x + y if op == 'plus' else x * y
        #return render_template('result3.html', x=x, y=y, op=op, result=result)
        return Response(
                    render_template('result3.html', x=x, y=y, op=op, result=result),
                    mimetype='text/html')


api.add_resource(Home, '/')
api.add_resource(CalculatorResult, '/multiply/')


if __name__ == '__main__':
    app.run(debug=True, port=5000)


'''
curl http://127.0.0.1:5000/multiply -H "Content-Type: application/json" -d '{"operator": "plus", "x": 2, "y": 3}'
'''
