from flask import Flask


app = Flask(__name__)


@app.route("/hello")
def hello() -> str:
    """
    Handle requests to the /hello endpoint.
    Returns:
        str: HTML paragraph containing a greeting message.
    """
    return "<p> Hello, </p>"


@app.route("/world")
def world() -> str:
    """
    Handle requests to the /world endpoint.
    Returns:
        str: HTML paragraph containing "World!" message.
    """
    return "<p>World!</p>"

@app.route("/")
def home_page() -> str:
    """
    Handle requests to the root endpoint.
    Returns:
        str: Welcome message for the homepage.
    """
    return "Welcome to the homepage."
