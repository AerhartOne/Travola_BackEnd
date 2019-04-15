from flask import Blueprint, request
from flask.json import jsonify
from flask_login import current_user
from models.trip import Trip
from models.trip_event import TripEvent
from models.user_trips import UserTrip
from models.user import User


trips_api_blueprint = Blueprint('trips_api',
                             __name__,
                             template_folder='templates')

@trips_api_blueprint.route('/', methods=['GET'])
def index():
    trip_query = Trip.select()
    trip_list = []
    for t in trip_query:
        trip_list.append( t.as_json_dict() )
    return jsonify( trip_list )

# Creates a new Trip object and saves it to the DB.
# Doesn't yet have any validation for trip_name.
# Doesn't yet validate if a user is logged in.
@trips_api_blueprint.route('/new', methods=['POST'])
def create():
    Trip.create(
        trip_name=request['trip_name'],
        parent_user=current_user.id
    )

# Deletes trip object from the DB with the given ID.
# Doesn't yet have any validation for trip_name.
# Doesn't yet validate if a user is logged in.
@trips_api_blueprint.route('/delete', methods=['POST'])
def delete():
    deletion_id = int( request.form['trip_id'] )
    Trip.delete().where(
        Trip.id==deletion_id
    ).execute()

@trips_api_blueprint.route('/<trip_id>/users/add', methods=['POST'])
def add_user(trip_id):
    user_id = request.form['user_id']
    user_object = User.get_or_none(User.id == user_id)
    if (user_object != None):
        UserTrip.create(user=user_object.id, trip=trip_id)

@trips_api_blueprint.route('/<trip_id>/users/delete', methods=['POST'])
def remove_user(trip_id):
    user_id = request.form['user_id']
    UserTrip.delete().where( UserTrip.trip == trip_id & UserTrip.user == user_id ).execute()

@trips_api_blueprint.route('/<trip_id>/events', methods=['GET'])
def events(trip_id):
    selected_events = TripEvent.select().where(TripEvent.parent_trip_id == trip_id)
    event_list = []
    for e in selected_events:
        event_list.append( e.as_json_dict() )
    return event_list
