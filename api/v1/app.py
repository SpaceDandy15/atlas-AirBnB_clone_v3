#!/usr/bin/python3
"""
This module defines the Flask app for the API,
including routes and error handlers.
It also configures CORS for cross-origin requests
and manages the database session
throughout the lifecycle of each request.

Flask app configuration:
- Registers blueprints for API routes
- Adds CORS support for handling cross-origin requests
- Provides error handlers for HTTP 404 and 405 errors
"""

from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS to allow cross-origin requests
from models import storage
from api.v1.views import app_views

# Create the Flask application
app = Flask(__name__)

# Enable CORS for all routes under /api/v1/*
# This allows any origin to make requests to the API
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


# Register the blueprint for handling API routes
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    This function is called after every request.
    It closes the session for the storage
    to ensure proper cleanup.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Custom error handler for 404 Not Found.
    Returns a JSON response indicating the resource was not found.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """
    Custom error handler for 405 Method Not Allowed.
    Returns a JSON response indicating the HTTP method is not allowed.
    """
    return jsonify({"error": "Method Not Allowed"}), 405


if __name__ == "__main__":
    """
    Starts the Flask web server. The app is set to run on 0.0.0.0 and port 5000
    with threaded mode enabled for handling multiple requests.
    """
    app.run(host="0.0.0.0", port=5000, threaded=True)
