#!/usr/bin/python3
"""Module for the cities view"""

from flask import Flask, jsonify, abort, request, Response
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route(
    '/states/<state_id>/cities',  strict_slashes=False, methods=['GET'])
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    dict_city = storage.all(City)
    cities_list = []
    for value in dict_city.values():
        if value.state_id == state_id:
            cities_list.append(value.to_dict())
    if cities_list == []:
        abort(404)
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """Retrieves a City object """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@ app_views.route(
    '/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return {}, 200


@ app_views.route(
    '/states/<state_id>/cities', strict_slashes=False, methods=['POST'])
def post_city(state_id):
    """Creates a City"""
    state = storage.get('State', state_id)
    if not request.get_json():
        abort(Response("Not a JSON", 400))
    elif "name" not in request.get_json():
        abort(Response("Missing name", 400))
    elif state is None:
        abort(404)
    else:
        new_city = City(**request.get_json())
        setattr(new_city, 'state_id', state_id)
        storage.new(new_city)
        storage.save()
    return new_city.to_dict(), 201


@ app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def put_city(city_id):
    """Updates a City object"""
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
            request.get_json().pop("state_id")
        except:
            pass

        city = storage.get('City', city_id)
        if city is None:
            abort(404)

        for key, value in request.get_json().items():
            setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
