from flask import Blueprint
from flask.json import jsonify
from models.trip_event import TripEvent

trip_events_api_blueprint = Blueprint('trip_events_api',
                             __name__,
                             template_folder='templates')

@trip_events_api_blueprint.route('/', methods=['GET'])
def index():
    trip_event_list = jsonify( [ t.as_json_dict() for t in TripEvent.select() ] )
    result = jsonify({
        'data' : trip_event_list
    })
    return result
