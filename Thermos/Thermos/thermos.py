from flask import Flask, render_template, url_for, request, redirect, flash
from datetime import datetime
from logging import DEBUG

from Users import User
from forms import BookmarkForm

app  = Flask(__name__)
app.logger.setLevel(DEBUG)
app.config['SECRET_KEY'] = 'kjW\xf5\t\xa0\x060f;n:]\x02\xce\xd9O\xa1\xd1\xc0[\xc2\xb7\xfa'

bookmarks = []

def store_bookmark(url, description):
    bookmarks.append(dict(
        url = url,
        description = description,
        user = "Mayank",
        date = datetime.utcnow()
    ))

def new_bookmarks(num):
    return sorted(bookmarks, key = lambda bm: bm['date'], reverse = True)[:num]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = "Author Introduction", user = User('Mayank', 'Mishra', 'Data Science Engineer', 'B.Tech Computer Science', 'Shikohabad'), new_bookmarks = new_bookmarks(5))


@app.route('/add', methods = ['GET', 'POST'])
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        store_bookmark(url, description)
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
