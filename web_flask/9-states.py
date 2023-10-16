#!/usr/bin/python3
"""States and State"""
from models import storage
from models.state import State
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def list_states_id(id=None):
    '''Renders a HTML page that shows state info by its id,
    if present'''
    states = storage.all(State)
    if id:
        key = '{}.{}'.format('State', id)
        if key in states:
            states = states[key]
        else:
            states = None
    else:
        states = storage.all(State).values()
    return render_template('9-states.html', states=states, id=id)


@app.teardown_appcontext
def teardown(self):
    '''Removes the current SQLAlchemy Session'''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
