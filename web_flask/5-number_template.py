#!/usr/bin/python3
"""Is num ? html template"""
from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    '''Displays “Hello HBNB!”'''
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    '''Displays “HBNB”'''
    return "HBNB"


@app.route("/c/<string:text>", strict_slashes=False)
def cisfun(text):
    '''Displays “C ” followed by the <text> variable'''
    return "C " + escape(text.replace('_', ' '))


@app.route("/python", strict_slashes=False)
@app.route("/python/<string:text>", strict_slashes=False)
def pyiscool(text="is cool"):
    '''Displays “Python ” followed by the <text> variable'''
    return "Python " + escape(text.replace('_', ' '))


@app.route("/number/<int:n>", strict_slashes=False)
def is_num(n):
    '''Displays “<n> is a number” only if <n> is an integer'''
    return "{:d} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def is_num_html(n=None):
    '''Displays a HTML page only if <n> is an integer'''
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
