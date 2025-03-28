from flask import Flask


app = Flask(__name__)


@app.route("/hello")
def hello():
    return "<p> Hello, </p>"


@app.route("/world")
def world():
    return "<p>World!</p>"

@app.route("/")
def home_page():
    return "Welcome to the homepage."