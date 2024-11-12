#!/usr/bin/python3
"""This file defines the Flask app for the API"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# Registering the blueprint
app.register_blueprint(app_views)


# Teardown function to close the storage session after each request
@app.teardown_appcontext
def teardown(exception):
    """Close the storage session after every request"""
    storage.close()


# Custom error handler for 404 errors
@app.errorhandler(404)
def not_found(error):
    """Return a JSON-formatted 404 response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    # Run the Flask app with environment variables for host and port
    app.run(host="0.0.0.0", port=5000, threaded=True)
