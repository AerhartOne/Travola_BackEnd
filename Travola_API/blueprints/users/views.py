from flask import Blueprint
from models.user import User
from flask.json import jsonify

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"

@users_api_blueprint.route('/<id>', methods=['GET'])
def user_profile(id):
    target_user = User[id]
    user_as_json = jsonify(
        id=target_user.id,
        username=target_user.username,
        email=target_user.email
    )
    return user_as_json
