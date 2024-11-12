#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/stats', methods=['GET'])
def stats():
    """Return the count of each object type"""
    stats = {
        "users": storage.count("User"),
        "places": storage.count("Place"),
        "states": storage.count("State"),
        "cities": storage.count("City"),
        "amenities": storage.count("Amenity"),
        "reviews": storage.count("Review")
    }
    return jsonify(stats)