#!/usr/bin/python3
""" Index module  """

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

classes = {"Amenity": "amenities", "City": "cities", "Place": "places",
           "Review": "reviews", "State": "states", "User": "users"}


@app_views.route('/status', strict_slashes=False)
def status():
    """ Method that returns the status """
    return ({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ Method that retrieves the number of each objects by type """
    new_dict = {}
    for key, value in classes.items():
        new_dict[value] = storage.count(key)
    return jsonify(new_dict)
