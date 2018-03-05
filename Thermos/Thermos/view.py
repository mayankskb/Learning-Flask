import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, url_for, request, redirect, flash

from author import Author
from forms import BookmarkForm

################################################################################
#                               APP CONFIGURATIONS                             #
################################################################################
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Configure database
app.config['SECRET_KEY'] = 'kjW\xf5\t\xa0\x060f;n:]\x02\xce\xd9O\xa1\xd1\xc0[\xc2\xb7\xfa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)

from models import User, Bookmark

#Fake login
def logged_in_user():
    return User.query.filter_by(username = 'Mayank').first()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = "Author Introduction", \
    user = Author('Mayank', 'Mishra', 'Data Science Engineer', 'B.Tech Computer Science', 'Shikohabad'), \
    new_bookmarks = Bookmark.newest(5))


@app.route('/add', methods = ['GET', 'POST'])
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = Bookmark(user = logged_in_user(), url = url, description = description)
        db.session.add(bm)
        db.session.commit()
        flash("Stored bookmark '{}'".format(description))
        return redirect(url_for('index'))
    return render_template('add.html', form = form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
