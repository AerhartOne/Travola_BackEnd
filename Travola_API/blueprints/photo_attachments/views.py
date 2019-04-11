from flask import Blueprint
from models.photo_attachment import PhotoAttachment

photo_attachments_api_blueprint = Blueprint('photo_attachments_api',
                             __name__,
                             template_folder='templates')

@photo_attachments_api_blueprint.route('/', methods=['GET'])
def index():
    return "photo_attachments API"
