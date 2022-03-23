from package.database import db, User, Post
from flask.cli import with_appcontext
import click


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
