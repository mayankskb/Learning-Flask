from view import app, db
from models import User
from flask.ext.script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username = 'Mayank', email = 'mishmabhiyank@hotmail.com'))
    db.session.add(User(username = 'Arjen', email = 'arjen@ebhjbxample.com0'))
    db.session.commit()
    print('Initialized the database')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to loose your all data"):
        db.drop_all()
        print('Dropped the database')


if __name__ == '__main__':
    manager.run()
