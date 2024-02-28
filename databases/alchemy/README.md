# Databases in Flask - Flask SQLAlchemy


Flask SQLAlchemy is a Flask version of the SQLAlchemy Python toolkit [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/). Rather than messing around directly with SQLite or another database you should strongly consider using SQLAlchemy. One advantage is that you can experiment with an SQLite database and then update to PostgreSQL without major code changes.

The following pip command install Flask, SQLAlchemy and Flask SQLAlchemy.

```bash
$ pip install Flask==3.0.1
$ pip install Flask-SQLAlchemy==3.1.1
```

The blog examples below are partially based on [https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application), but mostly on tutorials from [Corey Shafer's channel](https://www.youtube.com/c/Coreyms/videos) on Youtube, which has excellent tutorials on Flask and other Python topics. In particular, check out [Part 4](https://www.youtube.com/watch?v=cYWiDiIUxQc) and [Part 5](https://www.youtube.com/watch?v=44PvX0Yv368) of the Flask series. However, these use older version of Flask and some things just don't work as they used to anymore.

This turorial assumes some basic knowledge of Flask.

## First blog: users, but no posts

In the same directory as this readme file, there is a script named `blog1.py` that defines the ultra-simplistic beginnings of a blog application with just a list of users and a database for it. We can get a list of users, get the information of one user, or add a user, that's all. To focus at the basics of how to tie in a database there is no attempt to produce any nice html, we just dump out print strings. Here is the file in its entirity.

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

@app.get('/')
def index():
    users = User.query.all()
    return f'{users}\n'

@app.get('/<string:name>')
def get_user(name):
    user = User.query.filter_by(username=name).first()
    return f'{user}\n'

@app.post('/<string:name>/<string:email>')
def add_user(name, email):
    user = User(username=name, email=email)
    db.session.add(user)
    db.session.commit()
    return f'{user}\n'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
 ```

Let's look at this in bits and pieces. After the imports you create your Flask application, set up some database configurations and initialize an empty database.

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

The second configuration setting defines a local path for the database. The prefix `sqlite:` specifies we use an SQLite database and the three slashes indicate a relative path so `db_users.sqlite` is assumed to be in a directory named `instances`, but at this point the database does not yet exist. The third setting is added because without it you get a depreciation warning, set it to True if you want to use the Flask-SQLAlchemy event system, which is unlikely. The last line creates a database object, but still does not create anything on disk.

When you print the `db` variable you will see something like:

```
<SQLAlchemy engine=sqlite:////Users/marc/Documents/flask/blog/db_users.sqlite>
```

Next up is the definition of table classes. An instance of `Model` associates a user-defined Python class with a database table and you can use an instance of the class to interact with the database. Note that `Model` is a class that is stored on an `SQLAlchemy` instance.

```python
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r %r>' % (self.username, self.email)
```

This connects the `User` class to a table in `db_users.sqlite` named `user`. There is a default mapping from class name to table name, converting names like `TableName` into `table_name`, you can use the `__tablename__` class attribute to override the default. As we will see later you can create instances of the class and insert them into the database, or retrieve records from the database as class instances, change the instance and then save the results to the database.


### Database creation

At this moment we still do not have a database, all we have is the definition of a Python class that models a database table. When running the script from the command line the if statement at the end takes care of this:

```python
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

The `db.create_all()` method creates the schema if they don't exist. This needs to be done before you start the application the first time. Note that creating the databse is done inside an application context. The fine points of this are not quite clear to me, what is clear that there is a lot of documentation out there where the context is not used, which used to work but not anymore.

We now do have a database on disk and you can access it from a terminal with the `sqlite3 db_users.sqlite` command and then print the schema.

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


### Database access and manippulation

The database is still empty. To add records you use the `/name/email` endpoint:

```python
@app.post('/<string:name>/<string:email>')
def add_user(name, email):
    user = User(username=name, email=email)
    db.session.add(user)
    db.session.commit()
    return f'{user}\n'
```

```bash
$ curl 127.0.0.1:5000/admin/admin@example.com -X POST
```

The method associated with the resource creates an instance of User, adds it to the database using the session object and commits the change. There will be nothing in the `user` table until you do the commit. What is interesting to note is that the User instance does not have an identifier at first since initialization on the Python end does not do that. It is not until after the commit that the identifier created by the database will be added to the User object.

As you see there is some database logic lurking in the `add_user()` method, in a larger application this would probably be delegated to a database module.

With some data entered it finally makes sense to query the database.

```python
@app.route('/')
def index():
    users = User.query.all()
    return f'{users}\n'

@app.route('/<string:name>')
def get_user(name):
    user = User.query.filter_by(username=name).first()
    return f'{user}\n'
```

The `User.query.all()` method returns a list of User objects and `User.query.filter_by()` returns a list-like object. You can access an index on either of them, but you can use `first()` only on the result of the latter. Note how the `User.query.filter_by()` is the equivalent of a select query with a where clause.


### Running the service

You can start the script from a terminal.

```bash
$ python blog1.py
```

And from another terminal you can ping the service.

```bash
$ curl http://127.0.0.1:5000/
$ curl http://127.0.0.1:5000/admin
$ curl -X POST http://127.0.0.1:5000/sue/sue@example.com
```

These URLs are all connected to routes defined in the application. In the first case we get a listing of all users, in the second we get the information from just one user and in the third we add a user with her email.


## Second blog: adding posts

In this section we create another mini-blog application in `blog2.py`, which is the same as `blog`.py` except that it adds posts to the blog. This application has a lot of overlap with the previous one and here we only look at the differences. The biggest change is in the definition of the databse model.

```python
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User(id={self.id} name={self.username} email={self.email} posts={self.posts})"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post(title={self.title} content={self.content}')"
```

We add a table of posts and a one-to-many relation between users and posts. The users and posts tables are mostly unsurprising new table models, but there are two new things here: (1) a relation is added to the user table, and (2) one of the columns for the posts table is a foreign key. Let's look at these.

For the User table we define another variable named `posts`.

```python
posts = db.relationship('Post', backref='author', lazy=True)
```

This is NOT a column and it will not be in the database. But it does add a relation between a user and their posts. In the user model 'Post' references the name of the model class. The actual value of `posts` will be the list of posts for a user, that is, a list of instances of Post. The relation also adds a back reference from the `Post` instance to the user, that is, when you have a `Post` instance you can access the `author` variable and get the user. But there is no `author` column in the posts table. With `lazy=True` all we say is that the information will only be extracted if you ask for it (when you first access the variable).

On the posts side we have a foreign key column.

```python
user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

In the foreign key `user.id` references the table name and column name in the database. As noticed before, Flask-SQLAlchemy will automatically map the camel-cased class name to lower-cased table name. Note that the foreign key is a database notion while the relation is a Python object.

With the new objects in place we can add posts with a new Flask resource:

```python
@app.post('/<string:name>/<string:post_title>/<string:post_content>')
def add_post(name, post_title, post_content):
    user = User.query.filter_by(username=name).first()
    post = Post(title=post_title, content=post_content, user_id=user.id)
    db.session.add(post)
    db.session.commit()
    return f'{user}\n'
```

```bash
$ curl -X POST http://127.0.0.1:5000/john/john@example.com
$ curl -X POST http://127.0.0.1:5000/john/byebye/country
```

There is no decent error handling in this so if you do something unexpected, like adding a post to a non-existing user, you get a nasty error.


## Third blog: like the first blog, but now as a package

So far the code has been all put together in one file, but for larger applications you want the model and routes separated out to their own modules. We do that here for `blog1.py` and for good measure throw in some error handling. Separating the code into logical parts is not trivial since there is some tight integration in the code above and it takes some work to avoid circular imports. Using a package is your best option, here is its structure:

```bash
.
├── README.md
├── blog
│   ├── __init__.py
│   ├── model.py
│   └── routes.db
└── run.py
```

We now have two modules in the package that are really focused on their main charge. In `blog/model.py` all we do is defining the database model. Since this is a user-defined class we can add methods that take care of all database-related issues.

```python
from blog import db
from sqlalchemy.exc import IntegrityError

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
            db.session.add(user)
            db.session.commit()
            return str(user)
        except IntegrityError as e:
            db.session.rollback()
            return e
```

And `blog/routes.py` has just the routes with all database-related functionality delegated to the model.

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

This simple application does not use any static files and templates, but if it did we would be adding directories `blog/static` and `blog/templates`.

The `blog/__init__.py` file ties everything together. It creates the application, defines all its configuration settings, creates the database for the application and sets up all the routes.

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

Note that when you create the `db` variable you do not have defined any tables yet, that happens when importing the `routes` module, which imports the definition of the user table in the `model.User` class. Having the import at the bottom is somewhat funky, but it is the only way to avoid circular imports.

Finally, all you need to do in the startup script `run.py` is to import the application and the database model and then create the database and start the application.

```python
from blog import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

Using the application is exactly the same as for `blog1.py`.

This simple application does not use any static files and templates, but if it did we would be adding directories `blog/static` and `blog/templates`.

