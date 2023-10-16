#!/usr/bin/python3
"""HBNB filters"""
from models import storage
from models.amenity import Amenity
from models.city import City
from models.state import State
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def filters():
    '''Renders a HTML page using web_static files'''
    states = storage.all(State).values()
    cities = storage.all(City).values()
    amenities = storage.all(Amenity).values()
    return render_template(
        '10-hbnb_filters.html', states=states,
        cities=cities, amenities=amenities)


@app.teardown_appcontext
def teardown(self):
    '''Removes the current SQLAlchemy Session'''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
