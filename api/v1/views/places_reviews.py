#!/usr/bin/python3
"""This file handles RESTful actions for Review objects under places."""

from flask import request, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from werkzeug.exceptions import NotFound, BadRequest


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews_for_place(place_id):
    """Retrieves a list of all Review objects for a specific Place"""
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound("Place not found")

    reviews = storage.all(Review)
    place_reviews = [review.to_dict() for review in reviews.values()
                     if review.place_id == place.id]
    return jsonify(place_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a specific Review object"""
    review = storage.get(Review, review_id)
    if not review:
        raise NotFound("Review not found")
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a specific Review object"""
    review = storage.get(Review, review_id)
    if not review:
        raise NotFound("Review not found")

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a new Review for a specific Place"""
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound("Place not found")

    try:
        request_data = request.get_json(silent=True)
    except Exception:
        raise BadRequest("Not a JSON")

    user_id = request_data.get("user_id")
    if not user_id:
        raise BadRequest("Missing user_id")

    user = storage.get(User, user_id)
    if not user:
        raise NotFound("User not found")

    text = request_data.get("text")
    if not text:
        raise BadRequest("Missing text")
    temp = {
        "user_id": user_id,
        "place_id": place_id,
        "text": text
    }
    new_review = Review(temp)
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates an existing Review object"""
    review = storage.get(Review, review_id)
    if not review:
        raise NotFound("Review not found")

    try:
        request_data = request.get_json(silent=True)
    except Exception:
        raise BadRequest("Not a JSON")

    for key, value in request_data.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict())
