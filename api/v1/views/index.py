#!/usr/bin/python3
"""This file defines routes for API version 1"""

from flask import jsonify
from api.v1.views import app_views  # Keep this import here

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the status of the API as a JSON object"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def count_each_model():
    '''Retrieve and return the number of each object by type'''
    
    # Defer the imports to avoid circular import
    from api.v1.views import storage, valid_models

    counts = {}
    model_names = {
        'User': 'users',
        'State': 'states',
        'City': 'cities',
        'Place': 'places',
        'Amenity': 'amenities',
        'Review': 'reviews'
    }
    for name, model in valid_models().items():
        count = storage.count(model)
        name = model_names.get(name)
        counts.update({name: count})
    return jsonify(counts)
