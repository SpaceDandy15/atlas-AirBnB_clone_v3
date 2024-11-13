from flask import Blueprint
from models import storage

# Create the blueprint for the app views
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Register the users routes with the blueprint
from api.v1.views.users import app as users_app  # Import users' app here
app_views.register_blueprint(users_app)

# Register other blueprints as needed
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.places import *