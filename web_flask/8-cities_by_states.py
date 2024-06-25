#!/usr/bin/python3
"""
Starts a Flask web application.

This script defines a basic Flask web server that serves a list of states
stored in a database when accessed at the /cities_by_states URL.

Usage:
    Start the server by running this script. It will listen on all interfaces
    (0.0.0.0) on port 5000.

Endpoints:
    /cities_by_states:
        Displays a sorted list of all State objects present in storage.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """
    Displays a sorted list of all State objects.

    This view function queries the storage for all State objects, then
    sorts them alphabetically by state name. It renders a template to
    display the sorted list of states.

    Returns:
        str: Rendered HTML template with the list of states.
    """
    states = storage.all(State).values()
    states = sorted(states, key=lambda x: x.name)
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def teardown(exception):
    """
    Closes the storage connection on teardown.

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
