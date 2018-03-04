from thermos import app, db
from flask.ext.script import Manager, prompt_bool

from logging import DEBUG

from thermos import db
from models import User


manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username = 'Mayank', email = 'mishmayank@hotmail.com'))
    db.session.add(User(username = 'Arjen', email = 'arjen@example.com0'))
    db.session.commit()
    print('Initialized the database')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to loose your all data"):
        db.drop_all()
        print('Dropped the database')


if __name__ == '__main__':
    manager.run()
