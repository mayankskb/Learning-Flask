from flask import Flask, render_template, url_for

app  = Flask(__name__)

class User:
    def __init__(self, firstname, lastname, occupation):
        self.firstname = firstname
        self.lastname = lastname
        self.occupation = occupation

    def Firstname(self):
        return "First Name : {} ".format(self.firstname)

    def Lastname(self):
        return "Last Name : {}".format(self.lastname)

    def Occupation(self):
        return "Occupation : {}".format(self.occupation)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = "Author Introduction", user = User('Mayank', 'Mishra', 'Data Science Engineer'))


if __name__ == "__main__":
    app.run(debug = True)
