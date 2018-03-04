
from datetime import datetime

from flask import render_template, url_for, request, redirect, flash
from logging import DEBUG


from author import Author
from forms import BookmarkForm


bookmarks = []

#def store_bookmark(url, description):
#    bookmarks.append(dict(
#        url = url,
#        user = "Mayank",
#        date = datetime.utcnow()
#    ))

#def new_bookmarks(num):
#    return sorted(bookmarks, key = lambda bm: bm['date'], reverse = True)[:num]

#Fake login
def logged_in_user():
    return User.query.filter_by(username = 'Mayank').first()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = "Author Introduction", user = Author('Mayank', 'Mishra', 'Data Science Engineer', 'B.Tech Computer Science', 'Shikohabad'), new_bookmarks = Bookmark.newest(5))


@app.route('/add', methods = ['GET', 'POST'])
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
#        store_bookmark(url, description)
        bm = Bookmark(user = logged_in_user(), url = url, description = description)
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
