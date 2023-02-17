# Databases in Flask - Flask SQLAlchemy


Flask SQLAlchemy is a Flask version of the SQLAlchemy Python toolkit [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/). Rather than messing around directly with SQLite or another database you should strongly consider using SQLAlchemy. One advantage is that you can experiment with an SQLite database and then update to PostgreSQL without major code changes.

The following pip commands install Flask, SQLAlchemy and Flask SQLAlchemy.

```bash
$ pip install Flask
$ pip install Flask-SQLAlchemy
```

The blog examples below are partially based on [https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application), but mostly on tutorials from [Corey Shafer's channel](https://www.youtube.com/c/Coreyms/videos) on Youtube, which has excellent tutorials on Flask and other Python topics. In particular, check out [Part 4](https://www.youtube.com/watch?v=cYWiDiIUxQc) and [Part 5](https://www.youtube.com/watch?v=44PvX0Yv368) of the Flask series. However, these use older version of Flask and some things just don't work as they used to anymore.


## First blog: users, but no posts

We have a script named `blog_user.py` that defines the ultra-simplistic beginnings of a blog application with just a list of users and a database for it. We can get a list of users, get the information of one user, or add a user, that's all. To focus at the basics of how to tie in a database there is no attempt to produce any nice html, we just dump out print strings.

 ```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fc3bb2a43ff1103895a4ee315ee27740'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_users.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r %r>' % (self.username, self.email)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return f'{User.query.all()}\n'

@app.route('/<string:name>')
def get_user(name):
    user = User.query.filter_by(username=name).first()
    return f'{user}\n'

@app.route('/<string:name>/<string:email>', methods=['POST'])
def add_user(name, email):
    user = User(username=name, email=email)
    db.session.add(user)
    db.session.commit()
    return f'{user}\n'


if __name__ == '__main__':
    app.run(debug=True)
 ```

Let's look at this in batches. After the imports you create your Flask application, set up some database configurations and initialize an empty database.

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fc3bb2a43ff1103895a4ee315ee27740'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_users.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
```

Handing in the name of the current module makes sure that the application can find all templates and static files, but in this very simple application we are actually not using those static files. The first configuration setting is for security, use the `secrets` module to generate a key and paste it in.

```python
>>> import secrets
>>> secrets.token_hex(16)
'fc3bb2a43ff1103895a4ee315ee27740'
```

The second configuration setting defines a local path for the database. The prefix `sqlite:` specifies we use an SQLite database and the three slashes indicate a relative path so `db_users.sqlite` is assumed to be in a directory named `instances`, but at this point the database does not exist yet. The third setting is added because without it you get a depreciation warning, set it to True if you want to use the Flask-SQLAlchemy event system, which is unlikely. The last line creates a database object, but still does not create anything on disk.

When you print the `db` variable you will see something like:

```
<SQLAlchemy engine=sqlite:////Users/marc/Documents/flask/blog/db_users.sqlite>
```

An instance of `Model` associates a user-defined Python class with a database table and you can use the instance to add, delete and update records in the database. Note that `Model` is a class that is stored on an `SQLAlchemy` instance.

```python
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r %r>' % (self.username, self.email)
```

This connects the `User` class to a table in `db_users.sqlite` named `user`. There is a default mapping from class name to table name, converting names like `TableName` into `table_name`, you can use the `__tablename__` class attribute to override the default. As we will see later you can create instances of the class and insert them into the database, or retrieve records from the database as class instances, change the instance and then save the results to the database.


### The view from the Python command line

At this moment we still do not have a database, all we have is the definition of a Python class that models a database table. From the Python prompt, you can load your database object and then initialize the actual SQLite database:

```python
>>> from blog_users import db
>>> db.create_all()
```

At this point there is a database on disk and you can access it from a terminal with the `sqlite3 db_users.sqlite` command and then print the schema.

```sql
sqlite> .schema
CREATE TABLE user (
	id INTEGER NOT NULL,
	username VARCHAR(80) NOT NULL,
	email VARCHAR(120) NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (username),
	UNIQUE (email)
);
```

The database is still empty. You can add records from the SQLite prompt but you will typically do that in Python, first by creating `User` objects and then putting them into the database.

```python
>>> from blog_users import User
>>> admin = User(username='admin', email='admin@example.com')
>>> guest = User(username='guest', email='guest@example.com')
>>> admin.id, admin.username, admin.email
(None, 'admin', 'admin@example.com')
>>> db.session.add(admin)
>>> db.session.add(guest)
>>> db.session.commit()
>>> admin.id, admin.username, admin.email
(1, 'admin', 'admin@example.com')
```

There will be nothing in the `user` table until you do the commit. Note how there at first was no value for `admin.id`, this is because the database creates a unique primary key when you do the insert. After the commit, that value is also available on the `User` instance. It is simple to access the table in the database with the `User.query` object.

```python
>>> User.query.all()
[<User 'admin' 'admin@example.com'>, <User 'guest' 'guest@example.com'>]
```

The `filter_by()` method is the equivalent of a select query with a where clause. Each element of the return set is an instance of the `User` class and acts like a regular python object.

```python
>>> result = User.query.filter_by(username='admin').first()
>>> admin == result
True
```

One thing to keep in mind is that `all()` returns a list, but `filter_by()` a list-like object. You can take the index on either of them, but you can use `first()` only on the result of the latter.


### Back to the script

The same kind of Python commands that we used while in the Python prompt we can use for the routes.

```python
@app.route('/')
def index():
    return f'{User.query.all()}\n'

@app.route('/<string:name>')
def get_user(name):
    user = User.query.filter_by(username=name).first()
    return f'{user}\n'

@app.route('/<string:name>/<string:email>', methods=['POST'])
def add_user(name, email):
    user = User(username=name, email=email)
    db.session.add(user)
    db.session.commit()
    return f'{user}\n'
```

There is some database logic lurking in the `add_user()` method, in a larger application this would be delegated to a database module.


### Running the service

Assuming you have created a database you can start the script from a terminal.

```bash
$ python blog_users.py
```

And from another terminal you can ping the service.

```bash
$ curl http://127.0.0.1:5000/
$ curl http://127.0.0.1:5000/admin
$ curl -X POST http://127.0.0.1:5000/sue/sue@example.com
```

These URLs are all connected to routes defined in the application. In the first case we get a listing of all users, in the second we get the information from just one user and in the third we add a user with her email.


## Second blog: adding posts

In this section we create another mini-blog application in `blog_users_posts.py` that adds posts to the blog. We only look at the database aspect and forget about the routes (and therefore you should not try to use curl to interact with the database).

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fc3bb2a43ff1103895a4ee315ee27740'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_users_posts.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}' posts={self.posts})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.content}')"
```

We add a table of posts and a one-to-many relation between users and posts. The posts table is a mostly unsurprising new table model, but there are two new things here: (1) a relation is added to the user table, and (2) one of the columns for the posts table is a foreign key. Let's look at these.

For the user table we define another variable named `posts`.

```python
posts = db.relationship('Post', backref='author', lazy=True)
```

This is NOT a column and it will not be in the database. But it does add a relation between a user and his/her posts. In the user model 'Post' references the name of the model class. The actual value of `posts` will be the list of posts for a user. The relation also adds a back reference from the `Post` instance to the user, that is, when you have a `Post` instance you can access the `author` variable and get the user. But there is no `author` column in the posts table. With `lazy=True` all we say is that the information will only be extracted if you ask for it (when you first access the variable).

On the posts side we have a foreign key column.

```python
user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

In the foreign key `user.id` references the table name and column name in the database (the foreign key is a database notion while the relation is a Python object notion).

Let's go into Python to illustrate all this. First we import what we need and create the database.

```python
>>> from blog_users_posts import db, User, Post
>>> db.create_all()
```

We can now add a user.

```python
>>> sue = User(username='sue', email="sue@example.com")
>>> db.session.add(sue)
>>> db.session.commit()
>>> sue
User('sue', 'sue@example.com' posts=[])
```

There are no posts for the new user, but there will be after we add some, and they will be available directly on the `User` instance via the `posts` instance variable.

```python
>>> post1 = Post(title="p1", content="stuff1", user_id=sue.id)
>>> post2 = Post(title="p2", content="stuff2", user_id=sue.id)
>>> db.session.add_all([post1, post2])
>>> db.session.commit()
>>> sue
User('sue', 'sue@example.com' posts=[Post('p1', 'stuff1'), Post('p2', 'stuff2')])
```


## Third blog: like the first blog, but now as a package

So far the code has been all put together in one file, but for larger applications you want the model and routes separated out to their own modules. We do that here and add some error handling. Separating the code into logical parts is not trivial since some are tightly integrated and it takes some work to avoid circular imports, and using a package is your best option. The structure of the application is as follows.

```bash
.
├── README.md
├── blog
│   ├── __init__.py
│   ├── model.py
│   └── routes.db
└── run.py
```

First we go in to Python to create the database if it does not exist yet.

```python
>>> from blog import db
>>> from blog.model import User
>>> db.create_all()
>>> db.session.add(User(username='admin', email='admin@example.com'))
>>> db.session.add(User(username='guest', email='guest@example.com'))
>>> db.session.commit()
```

We now have the modules really focused on their main charge. In `blog/model.py` all we do is defining database model. Since this is a user-defined class we can add methods that take care of all database-related issues.

```python
from blog import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @classmethod
    def add(cls, name, email):
        try:
            user = User(username=name, email=email)
            print(user)
            db.session.add(user)
            db.session.commit()
            return str(user)
        except IntegrityError as e:
            db.session.rollback()
            return e
```

As before, the `blog/routes.py` has just the routes and all database related functionality is delegated to the model.

```python
from blog import app
from blog.model import User


@app.route('/')
def select_all():
    return '\n'.join([f'{row}' for row in User.query.all()]) + '\n'

@app.route('/<string:name>')
def select(name):
    user = User.query.filter_by(username=name).first()
    return f'{user}\n'

@app.route('/<string:name>/<string:email>', methods=['POST'])
def insert(name, email):
    result = User.add(name, email)
    return f'{result}\n'
```

The `blog/__init__.py` file ties this all together. It creates the application, defines all its configuration settings, creates the database for the application and sets up all the routes.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fc3bb2a43ff1103895a4ee315ee27740'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from blog import routes
```

Note that when you create the `db` variable you do not have defined any tables yet, that happens when importing `app.routes` which imports the definition of the user table in the `app.model.User` class.

Finally, all you need to do in `run.py` is a simple import and then invoke the `run()` command.

```python
from blog import app

if __name__ == '__main__':
    app.run(debug=True)
```

This simple application does not use any static files and templates, but if it did we would be adding directories `blog/static` and `blog/templates`.

