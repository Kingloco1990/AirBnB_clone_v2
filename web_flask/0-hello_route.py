#!/usr/bin/python3
"""
Starts a Flask web application.

This script defines a basic Flask web server that responds with "Hello HBNB!"
when accessed at the root URL.

Usage:
    Start the server by running this script. It will listen on all interfaces
    (0.0.0.0) on port 5000.

Endpoints:
    GET / - Returns a greeting message "Hello HBNB!".

"""

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """
    Handle GET requests on the root endpoint.

    Returns:
        str: A greeting message "Hello HBNB!".
    """
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
