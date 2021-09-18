#!/usr/bin/python3

from flask import Flask, jsonify, abort, request, Response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states',  strict_slashes=False, methods=['GET'])
def get_states():
    """ """
    dict_state = storage.all(State)
    states_list = []
    for value in dict_state.values():
        states_list.append(value.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """ """
    dict_state = storage.all(State)
    for key, value in dict_state.items():
        if "State.{}".format(state_id) == key:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """ """
    dict_state = storage.all(State)
    for key, value in dict_state.items():
        if "State.{}".format(state_id) == key:
            storage.delete(value)  # doesn't work
            return {}
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
    """ """
    if not request.get_json:
        abort(Response("Not a JSON", 400))
    elif not "name" in request.get_json:
        abort(Response("Missing name", 400))
    else:
        new_state = State(**request.get_json)
        storage.new(new_state)
        storage.save()
    return new_state.to_dict(), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def put_state(state_id):
    """ """
    if not request.get_json:
        abort(Response("Not a JSON", 400))
    else:
        dict_state = storage.all(State)
        for key, value in dict_state.items():
            if "State.{}".format(state_id) == key:
                return jsonify(value.to_dict())
        abort(404)
