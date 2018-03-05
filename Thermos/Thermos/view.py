import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, current_user, logout_user

from flask import render_template, url_for, request, redirect, flash

from author import Author
from forms import BookmarkForm, LoginForm

################################################################################
#                               APP CONFIGURATIONS                             #
################################################################################
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Configure database
app.config['SECRET_KEY'] = 'kjW\xf5\t\xa0\x060f;n:]\x02\xce\xd9O\xa1\xd1\xc0[\xc2\xb7\xfa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)

#configuring authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

from models import User, Bookmark

#Fake login
#def logged_in_user():
#    return User.query.filter_by(username = 'Mayank').first()

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = "Author Introduction", \
    user = Author('Mayank', 'Mishra', 'Data Science Engineer', 'B.Tech Computer Science', 'Shikohabad'), \
    new_bookmarks = Bookmark.newest(5))


@app.route('/add', methods = ['GET', 'POST'])
@login_required
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = Bookmark(user = current_user, url = url, description = description)
#        bm = Bookmark(user = logged_in_user(), url = url, description = description)
        db.session.add(bm)
        db.session.commit()
        flash("Stored bookmark '{}'".format(description))
        return redirect(url_for('index'))
    return render_template('add.html', form = form)

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    return render_template('user.html', user = user)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #login user and validate user...
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None:
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}".format(user.username))
            return redirect(request.args.get('next') or url_for('index'))
        flash('Incorrect username or password.')
    return render_template("login.html", form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
