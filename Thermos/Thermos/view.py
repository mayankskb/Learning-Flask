import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from flask.ext.moment import Moment

from flask import render_template, url_for, request, redirect, flash, abort

from author import Author

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

#for displaying the timestamps
moment = Moment(app)

from models import User, Bookmark, Tag
from forms import BookmarkForm, LoginForm, SignUp

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
        tags = form.tags.data
        bm = Bookmark(user = current_user, url = url, description = description, tags = tags)
#        bm = Bookmark(user = logged_in_user(), url = url, description = description)
        db.session.add(bm)
        db.session.commit()
        flash("Stored bookmark '{}'".format(description))
        return redirect(url_for('index'))
    return render_template('bookmark_form.html', form = form, title = 'Add a Bookmark')

@app.route('/edit/{<int:bookmark_id>}', methods = ['GET', 'POST'])
@login_required
def edit_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    form = BookmarkForm(obj = bookmark)
    if form.validate_on_submit():
        form.populate_obj(bookmark)
        db.session.commit()
        flash("Stored bookmark '{}'".format(bookmark.description))
        return redirect(url_for('user', username = current_user.username))
    return render_template('bookmark_form.html', form = form, title = 'Edit Bookmark')

@app.route('/delete/<int:bookmark_id>', methods = ['GET', 'POST'])
@login_required
def delete_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    if request.method == "POST":
        db.session.delete(bookmark)
        db.session.commit()
        flash('Deleted : "{}"'.format(bookmark.description))
        return redirect(url_for('user', username = current_user.username))
    else:
        flash('Please confirm deleting the bookmark.')
    return render_template('confirm_delete.html', bookmark = bookmark, nolinks = True)

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    return render_template('user.html', user = user)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #login user and validate user...
#       user = User.query.filter_by(username = form.username.data).first()
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}".format(user.username))
            return redirect(request.args.get('next') or url_for('user', username = user.username))
        flash('Incorrect username or password.')
    return render_template("login.html", form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods = ['GET','POST'])
def signup():
    form = SignUp()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please Login.'.format(user.username))
        return redirect(url_for('login'))
    return render_template('signup.html', form = form)

@app.route('/tag/<name>')
def tag(name):
    tag = Tag.query.filter_by(name = name).first_or_404()
    return render_template('tag.html', tag = tag)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@app.context_processor
def inject_tags():
    return dict(all_tags = Tag.all)
