#!/usr/bin/python3
"""This file defines routes for API version 1"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """Returns the status of the API as a JSON object"""
    return jsonify({"status": "OK"})
