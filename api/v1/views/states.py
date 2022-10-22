#!/usr/bin/python3
"""This module handles states routes"""
from flask import abort, jsonify, make_response, request
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
        return make_response(jsonify(states), 200)
    elif request.method == 'POST':
        form_data = request.get_json(silent=True)
        if form_data is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in form_data:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        new_state = State(name=form_data.get('name'))
        new_state.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def state_route(state_id):
    """
    state_route

    :param state_id: is the id of the state
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    if request.method == 'GET':
        return make_response(jsonify(state.to_dict()), 200)
    elif request.method == 'DELETE':
        state.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        form_data = request.get_json(silent=True)
        if form_data is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, val in form_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, val)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
