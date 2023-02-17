# Databases in Flask - Straight up SQLite

Beyond in stalling Flask this has no extra requirements since SQLite support is part of the Python standard library.

```bash
$ pip install Flask
```


## Using SQLite with the Python command line

Let's run some minimal Python code that creates a database and interacts with it. The first thing you do is get a database connection which allows your code to interact with the database server, which in this case is on the same machine, but it need not be.

```python
>>> import sqlite3
>>> connection = sqlite3.connect('test.db')
>>> connection
<sqlite3.Connection object at 0x10d6bd7b0>
```

This connection is required to send commands and receive answers. The connection is to `test.db` file, which if it did not exist will be created by the `connect()` method, but it will be empty. So first we create a table.

```python
>>> connection.execute("CREATE TABLE people (name TEXT PRIMARY KEY, food TEXT);")
<sqlite3.Cursor object at 0x10f7797a0>
```

If `test.db` already existed and had a table named `people` then we would get an error. The `execute()` method returns a cursor, which is a result set of rows from the database. In this case that set is empty because the command we executed did not return any database rows. Now we put in a few rows.

```python
>>> connection.execute("INSERT INTO people VALUES (?, ?)", ('jane', 'paella'))
>>> connection.execute("INSERT INTO people VALUES (?, ?)", ('john', 'pizza'))
```

You could use something like `INSERT INTO people VALUES ('jane', 'paella')`, but that would be susceptible to [SQL injection](https://en.wikipedia.org/wiki/SQL_injection), so use the parametrized insert with the question marks. In both cases Python returns a cursor, but again it is empty. Let's now view our data. For that we use the cursor returned by the select query.

```python
>>> cursor = connection.execute("SELECT * FROM people;")
>>> cursor.fetchall()
[('jane', 'paella'), ('john', 'pizza')]
```

With `fetchall()` you get all the rows from the cursor. The result above looks good, but the data is actually not in the database yet, which you can confirm when you look at it from outside Python:

```
$> sqlite3 test.db
SQLite version 3.30.1 2019-10-10 20:19:45
Enter ".help" for usage hints.
sqlite> .schema
CREATE TABLE people (name TEXT PRIMARY KEY, food TEXT);
sqlite> select * from people;
sqlite>
```

The problem is that when you use the `execute()` method to insert rows you open a transaction or continue a transaction that was already opened. But that transaction is not completed until you commit your changes (or roll them back). When you look in your directory you will actually see a journal file named `test.db-journal` which has all the changes that are not committed yet. You can commit only from the code from where you did the insert, in this case from the Python prompt.

```python
>>> connection.commit()
```

Now the data will persist in the database.


## Embedding code in Python functions

Here is a fairly minimal script named `db.py` that also uses SQLite from Python, but now in a more useful and reusable manner. Below we have methods that include some error checking, take care of committing changes and provide abstractions of database operations.

```python
import sqlite3

CREATE_TABLE = "CREATE TABLE people (name TEXT PRIMARY KEY, food TEXT)"
SELECT_WHERE = "SELECT * FROM people WHERE name=?"
SELECT = "SELECT * FROM people"
INSERT = "INSERT INTO people VALUES (?, ?)"


class DatabaseConnection(object):

    def __init__(self, filename):
        self.connection = sqlite3.connect(filename, check_same_thread=False)

    def create_schema(self):
        try:
            self.connection.execute(CREATE_TABLE)
        except sqlite3.OperationalError:
            print("Warning: 'people' table was already created, ignoring...")

    def get(self, name=None):
        cursor = (self.connection.execute(SELECT_WHERE, (name,))
                  if name is not None else self.connection.execute(SELECT))
        return cursor.fetchall()

    def add(self, name, food):
        try:
            self.connection.execute(INSERT, (name, food))
            self.connection.commit()
        except sqlite3.IntegrityError:
            print("Warning: '%s' is already in the database, ignoring..." % name)
            self.connection.rollback()
```

With this code you can simplify your interactions with the database.

```python
>>> from db import DatabaseConnection
>>> conn = DatabaseConnection('test.db')
>>> conn.create_schema()
>>> conn.add('jane', 'paella')
>>> conn.add('john', 'pizza')
>>> conn.get()
[('jane', 'paella'), ('john', 'pizza')]
```

A note on cursors. Above we have used the cursor just to get rows from the query result. In many Python tutorials you see the cursor used to create tables and execute select and insert queries. That is a not what a cursor usually is understood to be in database speak. If you choose to use a cursor to execute commands, it is generally better to not reuse it and create a new one with the `cursor()` method on the connection.


## Accessing the database code from Flask

We assume that we have a database with schema, but no data, in `people.sqlite`.

```python
>>> import db
>>> connection = db.DatabaseConnection('people.sqlite')
>>> connection.create_schema()
```

With all the database code in place it is easy to write the application.

```python
from flask import Flask
import db

app = Flask(__name__)
connection = db.DatabaseConnection('people.sqlite')

@app.route('/')
def all():
    rows = connection.get()
    return f'{rows}\n'

@app.route('/<string:name>')
def person(name):
    rows = connection.get(name)
    return f'{rows}\n'

@app.route('/<string:name>/<string:food>', methods=['POST'])
def add_person(name, food):
    connection.add(name, food)
    rows = connection.get(name)
    return f'{rows}\n'


if __name__ == '__main__':
    app.run(debug=True)
```

Now we start the server with `python app.py` and ping the application:

```bash
$ curl  http://127.0.0.1:5000/
```

When you do this you get a stack trace with at the end the following error.

```
sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread. The object was created in thread id 4577574400 and this is thread id 123145592672256.
```

What is going on is that the connection was first created in one thread (when you initialized the database connection when you loaded up the application) and then used from another thread (when you send the curl request which ultimately invoked the `get()` method). We need to make one little change so that the connection is sharable between threads. We change the initialization method of the `DatabaseConnection` class to disable thread checking.

```python
def __init__(self, filename):
    self.connection = sqlite3.connect(filename, check_same_thread=False)
```

After the automatic restart of the server it all works:

```bash
$ curl -X POST http://127.0.0.1:5000/jane/paella
[('jane', 'paella')]
$ curl -X POST http://127.0.0.1:5000/john/pizza
[('john', 'pizza')]
$ curl http://127.0.0.1:5000/
[('jane', 'paella'),  ('john', 'pizza')]
```

It should be noted that once you are using multiple threads with the same connection you may get concurrency issues. In particular, writing operations may need to be serialized to avoid data corruption. On the other hand, the locking mechanism that kicks in when there is a journal file may prevent this. The fact is, for larger multi-user applications where users can add and update records you will probably not be using SQLite.


## Using Flask templates

The output we created is just a text string and is not HTML at all. For example, for the main index page we just return the string representation of the database rows.

```python
@app.route('/')
def all():
    rows = connection.get_all()
    return f'{rows}\n'
```

You are free to generate HTML right at this spot with something like the following.

```python
@app.route('/')
def all():
    rows = connection.get_all()
    return f"<html>\n<body>\n<h1>All rows</h1>\n{rows}\n</body>\n</html>\n"
```

We would have to add a lot of code if we want to make this all nice HTML with the rows put in an ordered list or a table. This is where Jinja templates come in. Templates allow you to mix code into a regular HTML file and to separate HTML design from your route logic. To do that we import `render_template` from `flask` and just hand over the `rows` variable into a Jinja template.

```python
@app.route('/')
def all():
    rows = connection.get_all()
    return render_template('people.html', people=rows)
```

Templates all live in the `templates` folder and we simply add `templates/people.html` with content like the following.

```html
<html>
<body>
    <h1>All database rows</h1>
    <table cellpadding="5" cellspacing="0" border="1">
        {% for person in people %}
        <tr>
            <td>{{ person[0] }}</td>
            <td>{{ person[1] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
```

In this template you have two kind of blocks. One has a for loop and it uses Jinja syntax (not Python syntax) with curly brackets and percentage signs. The block itself is opened with `{% for person in people %}` and closed with `{% endfor %}` and it can include HTML code and other blocks. In addition there are two instances of variable blocks with double curly brackets: `{{ person[0] }}` and `{{ person[1] }}`. These blocks allow you to print the variable to the output, but you can also access any property or index that you can access on the object that the variable refers to, including methods. Notice how the `rows` variable from the routing code is available under the `people` parameter name in the template.
