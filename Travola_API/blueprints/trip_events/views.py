from flask import Blueprint, request
from flask.json import jsonify
from models.trip_event import TripEvent
from models.file_attachment import FileAttachment
from models.photo_attachment import PhotoAttachment
from Travola_API.utils.AWSHelper import upload_to_s3, S3_BUCKET
from flask_jwt_extended import jwt_required
from app import geocoder

trip_events_api_blueprint = Blueprint('trip_events_api',
                             __name__,
                             template_folder='templates')

@trip_events_api_blueprint.route('/', methods=['GET'])
def index():
    trip_event_list = [ t.as_dict() for t in TripEvent.select() ]
    result = jsonify({
        'data' : trip_event_list
    })
    return result

@trip_events_api_blueprint.route('/<id>', methods=['GET'])
def show(id):
    selected_trip = TripEvent.get_or_none(TripEvent.id == id)
    found_trip = (selected_trip != None)
    return_dict = None
    if (found_trip):
        selected_trip.as_dict()
    result = jsonify({
        'status' : found_trip,
        'data' : return_dict
    })
    return result

@trip_events_api_blueprint.route('/new', methods=['POST'])
@jwt_required
def create():
    data = request.form
    new_trip_event = TripEvent.create(
        parent_trip = data['parent_trip'],
        event_name = data['event_name'],
        date_time = data['date_time'],
        location_address = data['location_address'],
        latitude = data['latitude'],
        longitude = data['longitude'],
        desc = data['desc']
    )

    result = jsonify({
        'status' : True,
        'data' : new_trip_event.as_dict()
    })
    return result

@trip_events_api_blueprint.route('/delete', methods=['POST'])
@jwt_required
def delete():
    id_to_delete = request.form['trip_event_id']
    FileAttachment.delete().where(FileAttachment.parent_event == id_to_delete).execute()
    PhotoAttachment.delete().where(PhotoAttachment.parent_event == id_to_delete).execute()
    TripEvent.delete().where(TripEvent.id == id_to_delete).execute()

    trip_deleted = TripEvent.get_or_none(TripEvent.id == id_to_delete) == None

    result = jsonify({
        'status' : trip_deleted,
    })
    return result

@trip_events_api_blueprint.route('/<id>/edit', methods=['POST'])
def edit(id):
    data = request.form
    selected_trip_event = TripEvent.get_or_none(TripEvent.id == id)
    found_selected_trip = (selected_trip_event != None)
    return_dict = None
    if (found_selected_trip):
        selected_trip_event.event_name = data['event_name']
        selected_trip_event.date_time = data['date_time']
        selected_trip_event.location_address = data['location_address']
        selected_trip_event.latitude = data['latitude']
        selected_trip_event.longitude = data['longitude']
        selected_trip_event.desc = data['desc']
        selected_trip_event.save()
        return_dict = selected_trip_event.as_dict()

    result = jsonify({
        'status' : found_selected_trip,
        'data' : return_dict
    })
    return result

@trip_events_api_blueprint.route('/<id>/files', methods=['GET'])
def files(id):
    selected_files = FileAttachment.select().where(FileAttachment.parent_event == id)
    file_list = [ f.as_dict() for f in selected_files ]
    result = jsonify({
        'data' : file_list
    })
    return result

@trip_events_api_blueprint.route('/<id>/photos', methods=['GET'])
def photos(id):
    selected_photos = PhotoAttachment.select().where(PhotoAttachment.parent_event == id)
    photo_list = [ f.as_dict() for f in selected_photos ]
    result = jsonify({
        'data' : photo_list
    })
    return result

@trip_events_api_blueprint.route('/<id>/files/new', methods=['POST'])
def new_file(id):
    trip_event = TripEvent.get_or_none(TripEvent.id == id)
    new_file = None

    if trip_event and 'file' in request.files:
        uploaded_file = request.files['file']
        parent_trip = trip_event.parent_trip
        parent_user = parent_trip.parent_user

        upload_to_s3(uploaded_file, S3_BUCKET, f'files/{parent_trip.id}/{trip_event.id}/{parent_user.id}' )
        new_file = FileAttachment.create(
            url = f"{parent_trip.id}/{trip_event.id}/{parent_user.id}/{uploaded_file.filename}",
            parent_event = trip_event.id,
            title = uploaded_file.filename
        )    

    file_uploaded = (new_file != None)
    returned_data = None
    if file_uploaded:
        returned_data = new_file.as_dict()

    result = jsonify({
        'status' : file_uploaded,
        'data' : returned_data
    })
    return result


@trip_events_api_blueprint.route('/<id>/photos/new', methods=['POST'])
def new_photo(id):
    trip_event = TripEvent.get_or_none(TripEvent.id == id)
    new_photo = None

    if trip_event and 'photo' in request.files:
        uploaded_photo = request.files['photo']
        parent_trip = trip_event.parent_trip
        parent_user = parent_trip.parent_user

        upload_to_s3(uploaded_photo, S3_BUCKET, f'photos/{parent_trip.id}/{trip_event.id}/{parent_user.id}' )
        new_photo = PhotoAttachment.create(
            url = f"{parent_trip.id}/{trip_event.id}/{parent_user.id}/{uploaded_photo.filename}",
            parent_event = trip_event.id,
            title = uploaded_photo.filename
        )    

    photo_uploaded = (new_photo != None)
    returned_data = None
    if photo_uploaded:
        returned_data = new_photo.as_dict()

    result = jsonify({
        'status' : photo_uploaded,
        'data' : returned_data
    })
    return result


## MAP STUFF
@trip_events_api_blueprint.route('/search', methods=['POST'])
def search():
    query = request.form.get('map_query')
    response = geocoder.forward(query)
    collection = response.json()
    collection['type'] == 'FeatureCollection'
    # first = response.geojson()['features'][0]
    ## coordinates are located in the 'features' -> 'center' key that contains 2 items(lat & long) in an array 
    latitude = response.geojson()['features'][0]['center'][0] ##LATITUDE COORDINATE
    longitude = response.geojson()['features'][0]['center'][1] ## LONGITUDE COORDINATE

    # return redirect(url_for('map', query=query, latitude=latitude, longitude=longitude, response=response))
    return jsonify({
        'latitude' : latitude,
        'longitude' : longitude
    })

# @trip_events_api_blueprints.route('/save_location/<query>', methods=['POST'])
# def save_location(query):
#     response = geocoder.forward(query)
#     latitude = response.geojson()['features'][0]['center'][0]
#     longitude = response.geojson()['features'][0]['center'][1]
#     first = response.geojson()['features'][0]
#     address = first['place_name']

    # updated_trip_event = TripEvent.update(longitude=longitude, latitude=latitude, location_address=address)
    
    # if updated_trip_event.execute():
    #     print('Successfully Saved Trip to DB')
    #     return redirect(url_for('map', query=query, first=first))
    # else:
    #     print('Failed to Save')
    #     return redirect(url_for('map', query=query, first=first))

