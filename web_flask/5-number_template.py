#!/usr/bin/python3
""" starts a Flask web application"""
from flask import Flask
from flask import render_template


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def index():
    """Display 'Hello HBNB!'"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """Displays 'HBNB'"""
    return "HBNB"


@app.route('/c/<text>')
def c(text):
    """Displays 'C' followed by text"""
    text = text.replace('_', ' ')
    return f"C {text}"


@app.route('/python')
@app.route('/python/<text>')
def python(text='is cool'):
    """Displays 'Python' followed by value of text"""
    text = text.replace('_', ' ')
    return f"Python {text}"


@app.route('/number/<int:n>')
def number(n):
    """Displays 'n' if it's a number."""
    return f"{n} is a number"


@app.route('/number_template/<int:n>')
def number_template(n):
    """Returns a number template"""
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
