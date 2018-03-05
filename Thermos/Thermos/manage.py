from view import app, db
from models import User
from flask.ext.script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
    print('Initializing ......')
    db.create_all()
    print('Initialized the database')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to loose your all data"):
        db.drop_all()
        print('Dropped the database')


if __name__ == '__main__':
    manager.run()
