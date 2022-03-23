from  . import errors
from flask import render_template
from package.database import db,  User, Post


@errors.app_errorhandler(404)
def error(e):
    return render_template('404.html')


@errors.app_errorhandler(500)
def error(e):
    return render_template('500.html')

@errors.app_errorhandler(403)
def error(e):
    return render_template('500.html')


@errors.app_context_processor
def shell_context():
    return dict(db=db, User=User, Post=Post)

