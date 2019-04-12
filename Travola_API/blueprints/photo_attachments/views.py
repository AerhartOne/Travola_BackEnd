from flask import Blueprint
from flask.json import jsonify
from models.photo_attachment import PhotoAttachment

photo_attachments_api_blueprint = Blueprint('photo_attachments_api',
                             __name__,
                             template_folder='templates')

@photo_attachments_api_blueprint.route('/', methods=['GET'])
def index():
    return "photo_attachments API"

@photo_attachments_api_blueprint.route('/event/<id>', methods=['GET'])
def event_files(id):
    selected_files = PhotoAttachment.select().where(PhotoAttachment.parent_event==id)
    file_list = []
    for f in selected_files:
        file_list.append( f.as_json_dict() )
    return jsonify(file_list)