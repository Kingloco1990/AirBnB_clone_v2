#!/usr/bin/python3
"""
Flask Web Application

This script initializes a Flask web application with the following endpoints:

1. GET /:
   - Returns a greeting message "Hello HBNB!" when accessed.

2. GET /hbnb:
   - Returns the string "HBNB" when accessed.

3. GET /c/<text>:
   - Returns the string "C" followed by the value of the text variable
     with underscores replaced by spaces.

Usage:
    Start the server by running this script. It listens on all interfaces
    (0.0.0.0) on port 5000.

Endpoints:
    - GET / - Returns "Hello HBNB!".
    - GET /hbnb - Returns "HBNB".
    - GET /c/<text> - Returns "C <text>", where <text> is a string with
      underscores replaced by spaces.

"""

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """
    Handle GET requests on the root endpoint.

    Returns:
        str: A greeting message "Hello HBNB!".
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    Handle GET requests on the /hbnb endpoint.

    Returns:
        str: The string "HBNB".
    """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    """
    Handle GET requests on the /c/<text> endpoint.

    Args:
        text (str): The text to be displayed,
        with underscores replaced by spaces.

    Returns:
        str: The string "C <text>", where
        <text> has underscores replaced by spaces.
    """
    text = text.replace("_", " ")
    return f"C {text}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
