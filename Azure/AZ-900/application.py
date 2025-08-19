'''Creates a server that answers every request with a "Hello World!" message'''

from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    '''Return a friendly HTTP greeting.'''
    return "<html><body><h1>Hello Best Bike App!</h1></body></html>\n"
