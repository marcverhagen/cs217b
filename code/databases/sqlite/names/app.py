"""

Simple Flask app to insert rows and get a listing of all rows.

This folds functionality from insert.py, select_all.py and user_select2.py
into a Flask application.

Assumes the database was already created with create.py or names.sql.

This application has one endpoint, but it can be accessed with both a GET and
a POST request, where the first prints all rows and the second inserts a row
before printing all rows.

"""

import sqlite3
from flask import Flask, request, render_template


q_insert_name = "INSERT INTO names(name) VALUES (?)"
q_insert_name_address = "INSERT INTO names(name, address) VALUES (?, ?)"


app = Flask(__name__)
connection = sqlite3.connect('db-names.sqlite', check_same_thread=False)
cursor = connection.cursor()


def get_rows() -> list:
    """Get a list of tuples where each tuple represents a database row."""
    cursor.execute("SELECT * FROM names;")
    return cursor.fetchall()


def add_row(name: str, address: str):
    if address:
        cursor.execute(q_insert_name_address, (name, address))
    else:
        cursor.execute(q_insert_name, (name,))
    connection.commit()


@app.get('/')
def list():
    return render_template('index.html', rows=get_rows())


@app.post('/')
def add():
    name = request.form.get('name')
    address = request.form.get('address')
    add_row(name, address)
    return render_template('index.html', rows=get_rows())


if __name__ == '__main__':

    app.run(debug=True)
