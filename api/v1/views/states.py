from flask import Response, abort, json, jsonify, request
from werkzeug.wrappers import response
from api.v1.views import app_views

from models.state import State
from models import storage


@app_views.route('/states', methods=['GET', 'POST'])
def states_route():
    """
    states_route
    """
    if request.method == 'GET':
        states = list(map(lambda obj: obj.to_dict(),
                      storage.all(State).values()))
        return jsonify(states)
    elif request.method == 'POST':
        form_data = request.get_json(silent=True)
        if form_data is None:
            return Response('Not a json', status=400)
        if 'name' not in form_data:
            return Response('Missing name', status=400)
        new_state = State(name=form_data.get('name'))
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
def state_route(state_id):
    """
    state_route

    :param state_id: is the id of the state
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state)
        return jsonify({})
