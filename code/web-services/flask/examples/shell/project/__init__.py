import sys
import click

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __str__(self):
        return f'<User id={self.id} name={self.name}>'


def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)

    @app.get('/hello')
    def main():
        return "Hello"

    @app.cli.command("init")
    def init():
        """Create the database schema."""
        db.create_all()
        print('Schema created')

    @app.cli.command("reset")
    def reset():
        """Drop all tables and recreate the schema."""
        db.drop_all()
        db.create_all()

    @app.cli.command("users")
    def users():
        """List all users."""
        for user in User.query.all():
            print(user)

    @app.cli.command("add")
    @click.argument('name')
    def add(name):
        """Add a user."""
        user = User(name=name)
        db.session.add(user)
        db.session.commit()

    return app