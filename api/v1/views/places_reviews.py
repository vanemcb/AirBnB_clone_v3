#!/usr/bin/python3
"""Module for the places view"""

from flask import Flask, jsonify, abort, request, Response
from api.v1.views import app_views
from holberton_school.AirBnB_clone_v3.models import review
from models import storage
from models.review import Review


@app_views.route(
    '/places/<place_id>/reviews',  strict_slashes=False, methods=['GET'])
def get_reviews(place_id):
    """Retrieves the list of all Rewiew objects of a Place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    places_list = []
    for value in place.reviews:
        places_list.append(value.to_dict())
    return jsonify(places_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """Retrieves a Review object """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@ app_views.route(
    '/reviews/<review_id>', strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return {}, 200


@ app_views.route(
    '/places/<place_id>/reviews', strict_slashes=False, methods=['POST'])
def post_review(place_id):
    """Creates a Review in a place"""
    place = storage.get('Place', place_id)
    if not request.get_json():
        abort(Response("Not a JSON", 400))
    elif "user_id" not in request.get_json():
        abort(Response("Missing user_id", 400))
    elif storage.get('User', request.get_json().get('user_id')) is None:
        abort(404)
    elif "text" not in request.get_json():
        abort(Response("Missing text", 400))
    elif place is None:
        abort(404)
    else:
        new_review = Review(**request.get_json())
        setattr(new_review, 'place_id', place_id)
        storage.new(new_review)
        storage.save()
    return new_review.to_dict(), 201


@ app_views.route(
    '/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def put_review(review_id):
    """Updates a Review object"""
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
            request.get_json().pop("place_id")
        except:
            pass

        review = storage.get('Review', review_id)
        if review is None:
            abort(404)

        for key, value in request.get_json().items():
            setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
