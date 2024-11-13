#!/usr/bin/python3
"""New view for State objects that handles all default RESTFul API actions."""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects."""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object by ID."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by ID."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a new State object."""
    data = request.get_json(silent=True)  # silent=True prevents exception on bad JSON
    if data is None:
        abort(400, description="Not a JSON")  # 400 error if JSON is invalid or missing
    if "name" not in data:
        abort(400, description="Missing name")  # 400 error if 'name' field is missing
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates a State object by ID."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    
    # Ignore keys that shouldn't be updated
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    
    storage.save()
    return jsonify(state.to_dict()), 200
