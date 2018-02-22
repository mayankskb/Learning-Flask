from flask import Flask, render_template, url_for

app  = Flask(__name__)

class User:
    def __init__(self, firstname, lastname, occupation):
        self.firstname = firstname
        self.lastname = lastname
        self.occupation = occupation

    def Firstname(self):
        return "{} ".format(self.firstname)

    def Lastname(self):
        return "{}".format(self.lastname)

    def Occupation(self):
        return "{}".format(self.occupation)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = "Author Introduction", user = User('Mayank', 'Mishra', 'Data Science Engineer'))


@app.route('/add')
def add():
    return render_template('add.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug = True)
