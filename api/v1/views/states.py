#!/usr/bin/python3
"""This module handles states routes"""
from flask import Response, abort, json, jsonify, request
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
            return Response('Not a JSON', status=400)
        if 'name' not in form_data:
            return Response('Missing name', status=400)
        new_state = State(name=form_data.get('name'))
        new_state.save()
        return jsonify(new_state.to_dict()), 201


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
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        form_data = request.get_json(silent=True)
        if form_data is None:
            return Response('Not a JSON', status=400)
        for key, val in form_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, val)
        storage.save()
        return jsonify(state.to_dict()), 200
