from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from package import db
from package.database import User, Post


def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 )
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def posts(count=100):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(content=fake.text(),
                 title='Test Title',
                 user_id=u.id)
        db.session.add(p)
        db.session.commit()

