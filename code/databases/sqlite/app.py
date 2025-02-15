from flask import Flask, render_template
import db

app = Flask(__name__)
connection = db.DatabaseConnection('people.sqlite')

@app.get('/')
def index():
    rows = connection.get()
    return render_template('people.html', people=rows)

@app.get('/<string:name>')
def person(name):
    rows = connection.get(name)
    return f'{rows}\n'

@app.post('/<string:name>/<string:food>')
def add_person(name, food):
    success = connection.add(name, food)
    if success:
        return f"Added ('{name}', '{food}')\n"
    else:
        return f"Did not add ('{name}', '{food}')\n"

@app.get('/nasty/<string:name>/<string:food>')
def add_person_in_a_nasty_way(name, food):
    connection.add(name, food)
    rows = connection.get(name)
    return f'{rows}\n'


if __name__ == '__main__':
    app.run(debug=True)


"""
curl http://127.0.0.1:5000/
curl http://127.0.0.1:5000/jane
curl -X POST http://127.0.0.1:5000/john/bread
curl http://127.0.0.1:5000/nasty/john/bread
"""
