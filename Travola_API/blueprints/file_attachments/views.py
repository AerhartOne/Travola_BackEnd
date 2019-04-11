from flask import Blueprint
from models.file_attachment import FileAttachment

file_attachments_api_blueprint = Blueprint('file_attachments_api',
                             __name__,
                             template_folder='templates')

@file_attachments_api_blueprint.route('/', methods=['GET'])
def index():
    return "file_attachments API"
