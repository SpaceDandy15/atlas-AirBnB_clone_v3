#!/usr/bin/python3
"""
Module that handles all default RESTful API actions for Place objects.
"""

from flask import Flask, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import abort


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    """
    Retrieves a list of all Place objects for a given city.

    Args:
        city_id (str): The ID of the City object.

    Returns:
        JSON response containing a list of places for the specified city.

    Raises:
        404: If the city with the given city_id is not found.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404, description="City not found")

    places = storage.all(Place).values()
    places_list = [place.to_dict()
                   for place in places if place.city_id == city_id]

    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    Retrieves a Place object by its ID.

    Args:
        place_id (str): The ID of the Place object.

    Returns:
        JSON response with the Place object.

    Raises:
        404: If the place with the given place_id is not found.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes a Place object by its ID.

    Args:
        place_id (str): The ID of the Place object to delete.

    Returns:
        JSON response with an empty dictionary and a 200 status code.

    Raises:
        404: If the place with the given place_id is not found.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")

    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """
    Creates a new Place object for a given city.

    Args:
        city_id (str): The ID of the City to which the Place will be linked.

    Returns:
        JSON response with the new Place object and a 201 status code.

    Raises:
        404: If the city with the given city_id or
        user with user_id is not found.
        400: If the request is not valid JSON or
        required fields are missing.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404, description="City not found")

    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if not data.get('user_id'):
        abort(400, description="Missing user_id")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404, description="User not found")

    if not data.get('name'):
        abort(400, description="Missing name")

    place = Place(**data)
    place.city_id = city_id
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """
    Updates a Place object.

    Args:
        place_id (str): The ID of the Place object to update.

    Returns:
        JSON response with the updated Place object and a 200 status code.

    Raises:
        404: If the place with the given place_id is not found.
        400: If the request is not valid JSON.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")

    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200
