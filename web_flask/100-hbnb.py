#!/usr/bin/python3
"""
Starts a Flask web application.

This script initializes a Flask web server that serves the HBnB home page.
The application listens on all interfaces (0.0.0.0) on port 5000.

Usage:
    Start the server by running this script. It will listen on all interfaces
    (0.0.0.0) on port 5000.

Routes:
    /hbnb:
        Displays the main HBnB filters HTML page, including states, amenities,
        and places fetched from storage.
"""

from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    Displays the main HBnB filters HTML page.

    This view function queries the storage for all State, Amenity, and Place
    objects and renders a template to display them.

    Returns:
        str: Rendered HTML template with lists of states, amenities,
        and places.
    """
    states = storage.all("State")
    amenities = storage.all("Amenity")
    places = storage.all("Place")
    return render_template("100-hbnb.html",
                           states=states, amenities=amenities, places=places)


@app.teardown_appcontext
def teardown(exc):
    """
    Closes the current SQLAlchemy session.

    This function is called after each request to ensure that any
    open database connections are properly closed, preventing
    potential resource leaks.

    Args:
        exc (Exception): The exception that triggered the teardown,
            if any. Unused in this implementation.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
