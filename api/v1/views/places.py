#!/usr/bin/python3
"""Module for the places view"""

from flask import Flask, jsonify, abort, request, Response
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route(
    '/cities/<city_id>/places',  strict_slashes=False, methods=['GET'])
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    places_list = []
    for value in city.places:
        places_list.append(value.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@ app_views.route(
    '/places/<place_id>', strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return {}, 200


@ app_views.route(
    '/cities/<city_id>/places', strict_slashes=False, methods=['POST'])
def post_place(city_id):
    """Creates a place in a city"""
    city = storage.get('City', city_id)
    if not request.get_json():
        abort(Response("Not a JSON", 400))
    elif "user_id" not in request.get_json():
        abort(Response("Missing user_id", 400))
    elif storage.get('User', request.get_json().get('user_id')) is None:
        abort(404)
    elif "name" not in request.get_json():
        abort(Response("Missing name", 400))
    elif city is None:
        abort(404)
    else:
        new_place = Place(**request.get_json())
        setattr(new_place, 'city_id', city_id)
        storage.new(new_place)
        storage.save()
    return new_place.to_dict(), 201


@ app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def put_place(place_id):
    """Updates a Place object"""
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
        try:
            request.get_json().pop("user_id")
        except:
            pass
        try:
            request.get_json().pop("city_id")
        except:
            pass

        place = storage.get('Place', place_id)
        if place is None:
            abort(404)

        for key, value in request.get_json().items():
            setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
