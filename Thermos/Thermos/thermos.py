import os
from datetime import datetime

from flask import Flask, render_template, url_for, request, redirect, flash
from logging import DEBUG
from flask_sqlalchemy import SQLAlchemy

from author import Author
from forms import BookmarkForm
import models

basedir = os.path.abspath(os.path.dirname(__file__))

app  = Flask(__name__)
app.logger.setLevel(DEBUG)
app.config['SECRET_KEY'] = 'kjW\xf5\t\xa0\x060f;n:]\x02\xce\xd9O\xa1\xd1\xc0[\xc2\xb7\xfa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
db = SQLAlchemy(app)


bookmarks = []

#def store_bookmark(url, description):
#    bookmarks.append(dict(
#        url = url,
#        user = "Mayank",
#        date = datetime.utcnow()
#    ))

#def new_bookmarks(num):
#    return sorted(bookmarks, key = lambda bm: bm['date'], reverse = True)[:num]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = "Author Introduction", user = Author('Mayank', 'Mishra', 'Data Science Engineer', 'B.Tech Computer Science', 'Shikohabad'), new_bookmarks = models.Bookmark.newest(5))


@app.route('/add', methods = ['GET', 'POST'])
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
#        store_bookmark(url, description)
        bm = models.Bookmark(url = url, description = description)
        db.session.add(bm)
        db.session.commit()
        app.logger.debug('stored url : ' + url)
        app.logger.debug('description : ' + description)
        flash("Stored bookmark '{}'".format(description))
        return redirect(url_for('index'))
    return render_template('add.html', form = form)

#@app.route('/add', methods = ['GET', 'POST'])
#def add():
#    if request.method == "POST":
#        url = request.form['url']
#        store_bookmark(url)
#        app.logger.debug('stored url : ' + url)
#        flash("Stored bookmark '{}'".format(url))
#        return redirect(url_for('index'))
#    return render_template('add.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug = True)
