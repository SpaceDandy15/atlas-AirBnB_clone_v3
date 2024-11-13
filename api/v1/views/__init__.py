from flask import Blueprint
from models import storage

# Create the blueprint for the app views
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
storage = storage
validmodels = validmodels
# Register blueprints for different app modules
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.users import *
