from flask import Flask

# the flask application constructor
app = Flask(__name__)


# a view object
# object of app.route and tells that request coming to index page will be handled by this function
@app.route('/index')
def index():
    return 'Hello World'



if __name__ == "__main__":
    app.run()



# If you want to see how the flask server is responding or redirecting to these request
# use property app.url_map
