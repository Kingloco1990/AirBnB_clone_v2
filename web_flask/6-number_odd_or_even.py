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

4. GET /python/(<text>):
   - Returns the string "Python" followed by the value of the text variable
     with underscores replaced by spaces. Defaults to "is cool" if <text>
     is not provided.

5. GET /number/<n>:
   - Returns "<n> is a number" if <n> is an integer.

6. GET /number_template/<int:n>:
   - Renders an HTML page that displays the number <n>.

7. GET /number_odd_or_even/<int:n>:
   - Renders an HTML page that displays whether <n> is odd or even.

Usage:
    Start the server by running this script. It listens on all interfaces
    (0.0.0.0) on port 5000.

Endpoints:
    - GET / - Returns "Hello HBNB!".
    - GET /hbnb - Returns "HBNB".
    - GET /c/<text> - Returns "C <text>", where <text> is a string with
      underscores replaced by spaces.
    - GET /python/(<text>) - Returns "Python <text>", where <text> is a string
      with underscores replaced by spaces. Defaults to "is cool" if <text> is
      not provided.
    - GET /number/<n> - Returns "<n> is a number" if <n> is an integer.
    - GET /number_template/<int:n> - Renders an HTML page that displays
                                     the number <n>.
    - GET /number_odd_or_even/<int:n> - Renders an HTML page that displays
                                        whether <n> is odd or even.

"""

from flask import Flask, render_template

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
