#!/usr/bin/python3
"""This module handles states routes"""
from flask import Response, abort, json, jsonify, request
from werkzeug.wrappers import response
from api.v1.views import app_views

from models.user import User
from models import storage


@app_views.route('/users', methods=['GET', 'POST'])
def users_route():
    """
    users_route 
    """
    if request.method == 'GET':
        states = list(map(lambda obj: obj.to_dict(),
                      storage.all(User).values()))
        return jsonify(states)
    elif request.method == 'POST':
        form_data = request.get_json(silent=True)
        if form_data is None:
            return Response('Not a JSON', status=400)
        if 'name' not in form_data:
            return Response('Missing name', status=400)
        new_state = User(name=form_data.get('name'))
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user_route(user_id):
    """
    user_route 

    :param state_id: is the id of the user 
    """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        form_data = request.get_json(silent=True)
        if form_data is None:
            return Response('Not a JSON', status=400)
        for key, val in form_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, val)
        storage.save()
        return jsonify(user.to_dict()), 200

