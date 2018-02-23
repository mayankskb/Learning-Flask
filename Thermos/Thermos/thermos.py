from flask import Flask, render_template, url_for, request, redirect, flash
from datetime import datetime
from logging import DEBUG

app  = Flask(__name__)
app.logger.setLevel(DEBUG)
app.config['SECRET_KEY'] = 'kjW\xf5\t\xa0\x060f;n:]\x02\xce\xd9O\xa1\xd1\xc0[\xc2\xb7\xfa'

class User:
    def __init__(self, firstname, lastname, occupation, education, belonging):
        self.firstname = firstname
        self.lastname = lastname
        self.occupation = occupation
        self.education = education
        self.belonging = belonging

    def Firstname(self):
        return "{} ".format(self.firstname)

    def Lastname(self):
        return "{}".format(self.lastname)

    def Occupation(self):
        return "{}".format(self.occupation)

    def Education(self):
            return "{} ".format(self.education)

    def Belonging(self):
        return "{} ".format(self.belonging)


bookmarks = []

def store_bookmark(url):
    bookmarks.append(dict(
        url = url,
        user = "mayank",
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
    if request.method == "POST":
        url = request.form['url']
        store_bookmark(url)
        app.logger.debug('stored url : ' + url)
        flash("Stored bookmark '{}'".format(url))
        return redirect(url_for('index'))
    return render_template('add.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug = True)
