#!/usr/bin/python3
"""
Flask Web Application

This script initializes a Flask web application that responds to two endpoints:

1. GET /:
   - Returns a greeting message "Hello HBNB!" when accessed.

2. GET /hbnb:
   - Returns the string "HBNB" when accessed.

Usage:
    Start the server by running this script. It listens on all interfaces
    (0.0.0.0) on port 5000.

Endpoints:
    - GET / - Returns "Hello HBNB!".
    - GET /hbnb - Returns "HBNB".

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
