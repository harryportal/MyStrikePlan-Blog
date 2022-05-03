from package import db, login_manager
from datetime import datetime, timedelta
from flask_login import UserMixin
import jwt
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, unique=True, nullable=False)
    lastname = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    image = db.Column(db.String, nullable=False, default='default.jpg')
    password = db.Column(db.String)
    confirm = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_token(self):
        token = jwt.encode({'user_id': self.id, 'exp': datetime.utcnow() + timedelta(seconds=300)},
                           current_app.config['SECRET_KEY'], algorithm='HS256')
        return token

    def verify_user(self, token):
        try:
            decode = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return None
        user_id = decode['user_id']
        user = User.query.get(user_id)
        return user

    def __repr__(self):
        return f'User("{self.username}","{self.email}","{self.image}")'


class Post(db.Model):
    __tablename__ = 'Post'
    __searchable__ = ['title', 'content']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)


    def __repr__(self):
        return f'User("Title:{self.title} Content:{self.content}")'


