from flask import Blueprint
from models.trip_event import TripEvent

trip_events_api_blueprint = Blueprint('trip_events_api',
                             __name__,
                             template_folder='templates')

@trip_events_api_blueprint.route('/', methods=['GET'])
def index():
    return "trip_events API"
