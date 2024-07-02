#!/usr/bin/python3
"""
Starts a Flask web application.

This script defines a basic Flask web server that serves a list of states
stored in a database. The server listens on all interfaces (0.0.0.0)
on port 5000.

Usage:
    Start the server by running this script.

Endpoints:
    /states:
        Displays a sorted list of all State objects present in storage.
    /states/<id>:
        Displays the details of a State object with the specified ID.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """
    Displays a sorted list of all State objects.

    This view function queries the storage for all State objects, sorts them
    alphabetically by state name, and renders a template to display the sorted
    list of states.

    Returns:
        str: Rendered HTML template with the list of states.
    """
    states = storage.all(State).values()
    states = sorted(states, key=lambda x: x.name)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """
    Displays the details of a specific State object.

    This view function queries the storage for a State object with the given ID
    and renders a template to display its details.

    Args:
        id (str): The ID of the State object to retrieve.

    Returns:
        str: Rendered HTML template with the details of the State object, or
        a template with no state if the ID is not found.
    """
    for state in storage.all(State).values():
        if state.id == id:
            return render_template('9-states.html', state=state)
    return render_template('9-states.html')


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
