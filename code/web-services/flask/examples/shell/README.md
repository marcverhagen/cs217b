# Using the Flask Shell

Help on how to use the Flask shell, partially taken from a [YouTube video](https://www.youtube.com/watch?v=Wq6uflDfxf4) from Pretty Printed. Includes database creation and record insertion, as well as creation of custom commands. This video does things slightly differently from the way I usually do them so it gives another perspective.


### Preliminaries

Install some modules and initialize a flask environment file

```bash
pip install flask flask-sqlalchemy python-dotenv
touch .flaskenv
```

You also need a Flask application. Default names that Flask and the shell look for are `app.py` and `wsgi.py`. We will actually call this `run.py` so we have to put this in the environment:

```bash
FLASK_DEBUG = 1
FLASK_APP = run
```


### Minimal Flask application

Here is `run.py` with minimal app code:

```python
from flask import Flask
app = Flask(__name__)
```

You can now run the app with `flask run`, but there are no routes so when you ping the server you will get an error.

Let's change this a little and introduce a function `create_app()` that creates and returns the app as well as one route, and put this in a module called `project`:

```python
# project/__init__.py

from flask import Flask

def create_app():

	app = Flask(__name__)

	@app.get('/hello')
	def main():
		return "Hello"

	return app
```

And `run.py` app will just import `create_app` (Flask will also look for this factory function and use it to create the app):

```python
# run.py

from project import create_app
```


Flask will actually search for this function and use it so you won't even have to start the app manually. At this point you have an application with one route. 


### Some Flask commands

When you run `flask` you get a help message and will notice three basic commands: routes, run and shell. Here we list the routes, which apart from the one route in the app will also list the location of the static files:

```bash
$ flask routes
Endpoint  Methods  Rule
--------  -------  -----------------------
main      GET      /hello
static    GET      /static/<path:filename>
```

You can create extra commands right in your application by adding something like the following in `create_app()`, along the routes:

```python
@app.cli.command("create")
def create():
    print('Create command has run')
```

This is useful to do any setup actions you want to do from outside the app, like initializing data for example. This new command will be listed in the flask help, using the docstring as the description.


### Adding a database

For this you add an import, create a database and create a User class at the module level (from now only additions will be printed here, for the full file see the project's [init file](project/__init__.py)):

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
```

And within `create_app` you configure the app for the database and connect the database and the app:

```python
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://db.sqlite'
db.init_db(app)
```

Let's now use the shell which you start with `flask shell` (note that this depends on the flask environment including a value for FLASK_APP, as mentioned above). After starting the shell you get a specialized Python prompt which will set up a context for you that provides access to the resources you need. Some variables have been automatically imported, including app, db, User and Flask.g.

Here we are using the shell to initialize the database and add a user:

```python
>>> db.create_all()
>>> user = User(name='Sue')
>>> user
<User (transient 4431147984)>
>>> user.name
'Sue'
>>> db.session.add(user)
>>> user
<User (pending 4431147984)>
>>> db.session.commit()
>>> user
<User 1>
```

You can see that adding a user is a three-step process:

1. Creating an instance of the User class. The shell prints this in a particular way (which is actually different from what you get in a regular Python prompt). At that point the user has a name, but not yet an id.
2. Adding the user to the database. The user still has no id and if you were to open an sqlite prompt you would still not see the user.
3. Commiting the transaction. Now the user has an id and now you can see it at the sqlite prompt as well.

Above it was mentioned that you can create custom flask commands. Here is one that would create the database schema:

```python
@app.cli.command("init")
def init():
    """Create the database schema."""
    db.create_all()
    print('Schema created')
```

```bash
$  flask init
Schema created
```