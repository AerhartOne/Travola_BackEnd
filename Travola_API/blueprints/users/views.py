from flask import Blueprint, request, flash
from models.user import User
from models.trip import Trip
from flask.json import jsonify
from flask_login import login_user, logout_user, current_user

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"

@users_api_blueprint.route('/<id>', methods=['GET'])
def show(id):
    target_user_object = User.get_or_none(User.id == id)
    user_exists = (target_user_object != None)

    result = jsonify({
        'status' : user_exists,
        'data' : target_user_object.as_dict()
    })

    return result

### CREATE USER 
@users_api_blueprint.route('/', methods=['POST'])
def create():
    if request.form['password'] == request.form['re_password']:
        new_user = User(
            first_name = request.form['first_name'],
            last_name = request.form['last_name'],
            email = request.form['email'] ,
            username = request.form['username'],
            password = request.form['password']
            )

        if new_user.save():
            login_user(new_user)

    successfully_created = (User.get_or_none( User.username ==  new_user.username ) != None)

    result = jsonify({
        'status' : successfully_created,
        'data' : new_user.as_dict()
    })
    return result

### LOGIN USER
@users_api_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user_object = User.get_or_none(User.username == username)
    user_found = (user_object != None)
    logged_in = False
    if user_object != None:
        if password == user_object.password:
            logged_in = login_user(user_object)

    result = jsonify({
        'status' : (user_found and logged_in),
        'data' : user_object.as_dict()
    })
    return result

### LOGOUT USER
@users_api_blueprint.route('/logout')
def logout():
    return jsonify({
        'status' : logout_user()
    })

### SHOW TRIPS
@users_api_blueprint.route('/<id>/trips', methods=['GET'])
def trips(id):
    selected_trips = Trip.select().where(Trip.parent_user_id==id)
    trip_list = [ t.as_dict() for t in selected_trips ]

    result = jsonify( {
        'data': trip_list
    } )
    return result

