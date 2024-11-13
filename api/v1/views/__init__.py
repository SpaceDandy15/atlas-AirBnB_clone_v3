from flask import Blueprint
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

# Create the blueprint for the app views
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


def valid_models():
    """Return a dictionary of model names to model classes."""
    return {
        'User': User,
        'State': State,
        'City': City,
        'Place': Place,
        'Amenity': Amenity,
        'Review': Review
    }

# Register blueprints for different app modules
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.users import *
