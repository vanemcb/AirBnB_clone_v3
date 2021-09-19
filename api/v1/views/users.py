#!/usr/bin/python3
"""Module for the users view"""

from flask import Flask, jsonify, abort, request, Response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users',  strict_slashes=False, methods=['GET'])
def get_users():
    """Retrieves the list of all User objects"""
    dict_user = storage.all(User)
    users_list = []
    for value in dict_user.values():
        ausers_list.append(value.to_dict())
    return jsonify(users_list)


@app_views.route(
    '/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """Retrieves an User object """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@ app_views.route(
    '/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """Deletes an User object"""
    user = storage.get('User', amenity_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return {}, 200


@ app_views.route('/users', strict_slashes=False, methods=['POST'])
def post_user():
    """Creates a User"""
    if not request.get_json():
        abort(Response("Not a JSON", 400))
    elif "name" not in request.get_json():
        abort(Response("Missing name", 400))
    else:
        new_user = User(**request.get_json())
        storage.new(new_user)
        storage.save()
    return new_user.to_dict(), 201


@ app_views.route(
    '/users/<user_id>', strict_slashes=False, methods=['PUT'])
def put_user(user_id):
    """Updates a User object"""
    if not request.get_json():
        abort(Response("Not a JSON", 400))
    else:
        try:
            request.get_json().pop("id")
        except(exception):
            pass
        try:
            request.get_json().pop("created_at")
        except(exception):
            pass
        try:
            request.get_json().pop("updated_at")
        except(exception):
            pass
        try:
            request.get_json().pop("email")
        except(exception):
            pass

        user = storage.get('User', user_id)
        if user is None:
            abort(404)

        for key, value in request.get_json().items():
            setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
