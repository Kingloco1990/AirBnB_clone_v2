#!/usr/bin/python3
"""
Starts a Flask web application.

This script defines a basic Flask web server that serves a list of states
stored in a database when accessed at the /hbnb_filters URL.

Usage:
    Start the server by running this script. It will listen on all interfaces
    (0.0.0.0) on port 5000.

Endpoints:
    /hbnb_filters:
        Displays a sorted list of all State objects and amenities.

        This endpoint queries the database for all State and Amenity objects,
        sorts them alphabetically by name, and renders a template to display
        the sorted lists.

Returns:
    str: Rendered HTML template with the sorted lists of states and amenities.
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """
    Displays a sorted list of all State and Amenity objects.

    This view function queries the database for all State and Amenity objects,
    sorts them alphabetically by name, and renders a template to display the
    sorted lists of states and amenities.

    Returns:
        str: Rendered HTML template with the sorted lists of states and
        amenities.
    """
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()

    states = sorted(states, key=lambda x: x.name)
    amenities = sorted(amenities, key=lambda x: x.name)

    return render_template('10-hbnb_filters.html',
                           states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(exception):
    """
    Closes the database connection on application teardown.

    This function is called after each request to ensure that any
    open database connections are properly closed, preventing
    potential resource leaks.

    Args:
        exception (Exception): The exception that triggered the teardown,
            if any. Unused in this implementation.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
