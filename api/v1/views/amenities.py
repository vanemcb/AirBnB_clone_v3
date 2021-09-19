#!/usr/bin/python3
"""Module for the cities view"""

from flask import Flask, jsonify, abort, request, Response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',  strict_slashes=False, methods=['GET'])
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    dict_amenity = storage.all(Amenity)
    amenities_list = []
    for value in dict_amenity.values():
        amenities_list.append(value.to_dict())
    return jsonify(amenities_list)


@app_views.route(
    '/amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves an Amenity object """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@ app_views.route(
    '/amenities/<amenity_id>', strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return {}, 200


@ app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def post_amenity():
    """Creates a Amenity"""
    if not request.get_json():
        abort(Response("Not a JSON", 400))
    elif "name" not in request.get_json():
        abort(Response("Missing name", 400))
    else:
        new_amenity = Amenity(**request.get_json())
        storage.new(new_amenity)
        storage.save()
    return new_amenity.to_dict(), 201


@ app_views.route(
    '/amenities/<amenity_id>', strict_slashes=False, methods=['PUT'])
def put_amenity(amenity_id):
    """Updates a Amenity object"""
    if not request.get_json():
        abort(Response("Not a JSON", 400))
    else:
        try:
            request.get_json().pop("id")
        except:
            pass
        try:
            request.get_json().pop("created_at")
        except:
            pass
        try:
            request.get_json().pop("updated_at")
        except:
            pass

        amenity = storage.get('Amenity', amenity_id)
        if amenity is None:
            abort(404)

        for key, value in request.get_json().items():
            setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
