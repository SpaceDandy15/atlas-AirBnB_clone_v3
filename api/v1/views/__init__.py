# api/v1/views/__init__.py
from flask import Blueprint

# Create the blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import everything from the index file to register routes
from api.v1.views.index import *
from api.v1.views.stats import *
from api.v1.views.states import *
