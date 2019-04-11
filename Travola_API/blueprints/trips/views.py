from flask import Blueprint
from models.trip import Trip

trips_api_blueprint = Blueprint('trips_api',
                             __name__,
                             template_folder='templates')

@trips_api_blueprint.route('/', methods=['GET'])
def index():
    return "trips API"
