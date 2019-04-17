from flask import Blueprint, request
from flask.json import jsonify
from models.trip_event import TripEvent
from models.file_attachment import FileAttachment
from models.photo_attachment import PhotoAttachment
import Travola_API.utils.trip_event_notify_helper

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