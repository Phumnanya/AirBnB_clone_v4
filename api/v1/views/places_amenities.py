#!/usr/bin/python3
"""This module contains view for the link between Place objects and Amenity
objects that handle all default RESTFul API actions"""
import os
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def place_amenities_route(place_id):
    """
    place_amenities handles get request to /places/<place_id>/amenities

    :param place_id: is the id of the place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        amenities = list(
            map(lambda amenity: amenity.to_dict(), place.amenities))
        return make_response(jsonify(amenities), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def place_amenity(place_id, amenity_id):
    """
    place_amenity handles delete, post request to
    /places/<place_id>/amenities/<amenity_id>

    :param place_id: is the id of the place
    :param amenity_id: is the id of the amenity
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)
    amenities = place.amenities
    if request.method == 'DELETE':
        if amenity not in amenities:
            abort(404)
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            amenities.remove(amenity)
        else:
            del amenity.place_id
        place.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'POST':
        if amenity in amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            amenities.append(amenity)
        else:
            amenity.place_id = place.id
        place.save()
        return make_response(jsonify(amenity.to_dict()), 201)
