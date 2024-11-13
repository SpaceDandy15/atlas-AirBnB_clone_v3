#!/usr/bin/python3
"""
This module handles all default RESTful API actions for the User object.
It includes routes for getting, creating, updating, and deleting users.
"""

from flask import Flask, jsonify, request, abort
from models import storage
from models.user import User

app = Flask(__name__)


@app.route('/api/v1/users', methods=['GET'])
def get_users():
    """
    Retrieve the list of all User objects.

    Route responds to GET requests to fetch a list of all users in the system.
    It returns a JSON rep of all the users' data using the to_dict() method.
    """
    users = storage.all(User).values()  # Get all users as a list
    return jsonify([user.to_dict() for user in users])


@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieve a User object by its ID.

    Route responds to GET requests to fetch a user based on the user_id.
    If the user is not found, it raises a 404 error.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a User object by its ID.

    Route responds to DELETE requests to delete a user based on the user_id.
    If the user is not found, it raises a 404 error.
    After deletion, it returns an empty dictionary with a 200 status code.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    """
    Create a new User.

    This route responds to POST requests to create a new user.
    The request must include a valid JSON body with the keys
    'email' and 'password'. If any key is missing
    or the body is not valid JSON, it raises a 400 error.
    Returns the newly created user with a 201 status code.
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()

    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")

    user = User(**data)
    storage.new(user)
    storage.save()
    return user.to_dict, 201


@app.route('/api/v1/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update an existing User object.

    Route responds to PUT requests to update a user based on the user_id.
    Request must include valid JSON data,
    any fields such as 'id', 'email', 'created_at',
    and 'updated_at' will be ignored during the update.
    If the user is not found, it raises a 404 error.
    Returns the updated user object with a 200 status code.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
