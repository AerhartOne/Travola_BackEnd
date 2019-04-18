from flask import Blueprint, request
from flask.json import jsonify
from models.trip_event import TripEvent
from models.file_attachment import FileAttachment
from models.photo_attachment import PhotoAttachment
from Travola_API.utils.AWSHelper import upload_to_s3, S3_BUCKET

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
def create():
    data = request.form
    new_trip_event = TripEvent.create(
        parent_trip = data['parent_trip'],
        date_time = data['date_time'],
        location = data['location']
    )

    result = jsonify({
        'status' : True,
        'data' : new_trip_event.as_dict()
    })
    return result

@trip_events_api_blueprint.route('/delete', methods=['POST'])
def delete():
    id_to_delete = request.form['id']
    TripEvent.delete().where(TripEvent.id == id_to_delete)

    trip_deleted = TripEvent.get_or_none(id_to_delete) == None

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
        selected_trip_event.parent_trip = data['parent_trip']
        selected_trip_event.date_time = data['date_time']
        selected_trip_event.location = data['location']
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

    if trip_event and request.files['photo']:
        uploaded_file = request.files['photo']
        parent_trip = trip_event.parent_trip
        parent_user = parent_trip.parent_user

        upload_to_s3(uploaded_file, S3_BUCKET, f'photos/{parent_trip.id}/{trip_event.id}/{parent_user.id}' )
        new_file = FileAttachment.create(
            url = f"{parent_trip.id}/{trip_event.id}/{parent_user.id}/{uploaded_file.filename}",
            parent_user = parent_user.id
        )    

    file_uploaded = (new_file != None)

    result = jsonify({
        'status' : file_uploaded,
        'data' : new_file.as_dict()
    })
    return result


@trip_events_api_blueprint.route('/<id>/photos/new', methods=['POST'])
def new_photo(id):
    trip_event = TripEvent.get_or_none(TripEvent.id == id)
    new_photo = None

    if trip_event and request.files['photo']:
        uploaded_photo = request.files['photo']
        parent_trip = trip_event.parent_trip
        parent_user = parent_trip.parent_user

        upload_to_s3(uploaded_photo, S3_BUCKET, f'photos/{parent_trip.id}/{trip_event.id}/{parent_user.id}' )
        new_photo = PhotoAttachment.create(
            url = f"{parent_trip.id}/{trip_event.id}/{parent_user.id}/{uploaded_photo.filename}",
            parent_user = parent_user.id
        )    

    photo_uploaded = (new_photo != None)

    result = jsonify({
        'status' : photo_uploaded,
        'data' : new_photo.as_dict()
    })
    return result

