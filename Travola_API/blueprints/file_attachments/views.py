from flask import Blueprint
from flask.json import jsonify
from models.file_attachment import FileAttachment

file_attachments_api_blueprint = Blueprint('file_attachments_api',
                             __name__,
                             template_folder='templates')

@file_attachments_api_blueprint.route('/', methods=['GET'])
def index():
    return "file_attachments API"

@file_attachments_api_blueprint.route('/event/<id>', methods=['GET'])
def event_files(id):
    selected_files = FileAttachment.select().where(FileAttachment.parent_event==id)
    file_list = []
    for f in selected_files:
        file_list.append( f.as_dict() )
    return jsonify(file_list)