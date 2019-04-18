from flask import Blueprint, request
from flask.json import jsonify
from flask_login import current_user
from models.trip import Trip
from models.trip_event import TripEvent
from models.user_trip import UserTrip
from models.user import User
from Travola_API.utils.AWSHelper import upload_to_s3, S3_BUCKET

trips_api_blueprint = Blueprint('trips_api',
                             __name__,
                             template_folder='templates')

@trips_api_blueprint.route('/', methods=['GET'])
def index():
    trip_query = Trip.select()
    trip_list = []
    for t in trip_query:
        trip_list.append( t.as_dict() )

    result = jsonify( {
        'data': trip_list
        } )
    return result

@trips_api_blueprint.route('/<id>/show', methods=['GET'])
def show(id):
    trip = Trip.get_or_none(Trip.id==id)
    trip_found = trip != None
    result = jsonify({
        'status': trip_found,
        'data' : trip.as_dict()
    })
    return result

# Creates a new Trip object and saves it to the DB.
# Doesn't yet have any validation for trip_name.
# Doesn't yet validate if a user is logged in.
@trips_api_blueprint.route('/new', methods=['POST'])
def create():
    new_trip = Trip.create(
        trip_name=request.form['trip_name'],
        parent_user=request.form['user_id'],
        trip_desc=request.form['trip_desc'],
        trip_img_url=""
    )

    if request.files['trip_img']:
        uploaded_img = request.files['trip_img']
        upload_to_s3(uploaded_img, S3_BUCKET, f'trip_display_imgs/{new_trip.id}' )
        new_trip.trip_img_url = f'{new_trip.id}/{uploaded_img.filename}'
        new_trip.save()

    result = jsonify({
        'status': True,
        'data' : new_trip.as_dict()
    })
    return result

# Deletes trip object from the DB with the given ID.
# Doesn't yet have any validation for trip_name.
# Doesn't yet validate if a user is logged in.
@trips_api_blueprint.route('/delete', methods=['POST'])
def delete():
    deletion_id = int( request.form['trip_id'] )
    Trip.delete().where(
        Trip.id==deletion_id
    ).execute()

    successfully_deleted = Trip.get_or_none(Trip.id == deletion_id) == None

    result = jsonify({
        'status' : successfully_deleted
    })
    return result


@trips_api_blueprint.route('/<trip_id>/users/add', methods=['POST'])
def add_user(trip_id):
    user_id = request.form['user_id']
    user_object = User.get_or_none(User.id == user_id)
    user_trip_object = UserTrip.get_or_none(UserTrip.user == user_id & UserTrip.trip == trip_id)
    if (user_object != None and user_trip_object == None):
        user_trip_object = UserTrip.create(user=user_object.id, trip=trip_id)    
    
    successfully_created = (user_trip_object != None)

    result = jsonify({
        'status' : successfully_created,
        'data' : user_trip_object.as_dict()
    })
    return result

@trips_api_blueprint.route('/<trip_id>/users/delete', methods=['POST'])
def remove_user(trip_id):
    user_id = request.form['user_id']
    UserTrip.delete().where( UserTrip.trip == trip_id & UserTrip.user == user_id ).execute()

    successfully_deleted = UserTrip.get_or_none(UserTrip.user == user_id & UserTrip.trip == trip_id) == None

    result = jsonify({
        'status' : successfully_deleted
    })
    return result

@trips_api_blueprint.route('/<trip_id>/events', methods=['GET'])
def events(trip_id):
    selected_events = TripEvent.select().where(TripEvent.parent_trip_id == trip_id)
    event_list = []
    for e in selected_events:
        event_list.append( e.as_dict() )
    
    result = jsonify( {
        'data': event_list
        } )
    return result
