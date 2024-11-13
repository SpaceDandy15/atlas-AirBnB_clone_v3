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
    """
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieve a User object by its ID.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a User object by its ID.
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
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json(silent=True)

    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")

    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app.route('/api/v1/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update an existing User object.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json(silent=True)

    # Ignore the following fields for updates
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict())
