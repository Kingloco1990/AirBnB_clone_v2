#!/usr/bin/python3
"""
Starts a Flask web application.

This script defines a basic Flask web server that responds to various endpoints
with specific functionalities and templates.

Usage:
    Start the server by running this script. It will listen on all interfaces
    (0.0.0.0) on port 5000.

Endpoints:
    /: Root endpoint that returns a greeting message "Hello HBNB!".
    /hbnb: Endpoint that returns the string "HBNB".
    /c/<text>: Endpoint that returns a string starting with "C " followed by
               the provided <text> parameter with underscores replaced by
               spaces.
    /python/<text>: Endpoint that returns a string starting with "Python"
                    followed by the provided <text> parameter with underscores
                    replaced by spaces. Defaults to "is cool" if <text> is not
                    provided.
    /number/<int:n>: Endpoint that returns a string "<n> is a number" if <n>
                     is an integer.
    /number_template/<int:n>: Endpoint that renders an HTML template
                              displaying the number <n>.
    /number_odd_or_even/<int:n>: Endpoint that renders an HTML template
                                 displaying whether <n> is odd or even.
    /states_list: Endpoint that displays a list of all State objects present
                  in storage.
"""

from flask import Flask, render_template
from models import storage
from models.state import State


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
        text (str): The text to be displayed, with underscores
                    replaced by spaces.

    Returns:
        str: The string "C <text>", where <text> has underscores
             replaced by spaces.
    """
    text = text.replace("_", " ")
    return f"C {text}"


@app.route("/python/<text>", strict_slashes=False)
@app.route("/python/", strict_slashes=False)
def python_text(text="is cool"):
    """
    Handle GET requests on the /python/<text> endpoint.

    Args:
        text (str, optional): The text to be displayed, with underscores
                              replaced by spaces.
                              Defaults to "is cool" if not provided.

    Returns:
        str: The string "Python <text>", where <text> has
             underscores replaced by spaces.
    """
    text = text.replace("_", " ")
    return f"Python {text}"


@app.route("/number/<int:n>", strict_slashes=False)
def number_n(n):
    """
    Handle GET requests on the /number/<n> endpoint.

    Args:
        n (int): The number to be checked.

    Returns:
        str: The string "<n> is a number" if <n> is an integer.
    """
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template_n(n):
    """
    Handle GET requests on the /number_template/<int:n> endpoint.

    Args:
        n (int): The number to be displayed on the template.

    Returns:
        str: The rendered HTML template displaying the number <n>.
    """
    return render_template('5-number.html', n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even_n(n):
    """
    Handle GET requests on the /number_odd_or_even/<int:n> endpoint.

    Args:
        n (int): The number to check if it's odd or even.

    Returns:
        str: The rendered HTML template displaying whether <n> is odd or even.
    """
    return render_template('6-number_odd_or_even.html', n=n)


@app.route("/states_list", strict_slashes=False)
def state_list():
    """
    Displays a list of all State objects.

    This view function queries the storage for all State objects, then
    renders a template to display the list of states.

    Returns:
        str: Rendered HTML template with the list of states.
    """
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


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
