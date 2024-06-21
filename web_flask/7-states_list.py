#!/usr/bin/python3
"""
Starts a Flask web application.

This script defines a basic Flask web server that serves a list of states
stored in a database when accessed at the /states_list URL.

Usage:
    Start the server by running this script. It will listen on all interfaces
    (0.0.0.0) on port 5000.

Endpoints:
    /states_list: Displays a list of all State objects present in storage.
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def state_list():
    """
    Displays a list of all State objects.

    This view function queries the storage for all State objects, then
    renders a template to display the list of states.

    Returns:
        str: Rendered HTML template with the list of states.
    """
    states = storage.all(State).values() # Retrieve all State objects from storage
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(exception):
    """
    Closes the storage on teardown.

    This function is called after each request to close the storage,
    ensuring any database connections are properly closed.

    Args:
        exception (Exception): The exception that caused the teardown,
        if any.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
