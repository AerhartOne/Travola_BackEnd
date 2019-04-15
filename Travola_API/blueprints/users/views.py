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
def user_profile(id):
    target_user = User[id]
    user_as_json = jsonify(
        id=target_user.id,
        username=target_user.username,
        email=target_user.email
    )
    return user_as_json

### CREATE USER 
@users_api_blueprint.route('/', methods=['POST'])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email'] 
    username = request.form['username']
    password = request.form['password']
    re_password = request.form['re_password']

    user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)

    if user.save and password == re_password:
        login_user(user)
        # return jsonify({'status' : 'Successfully created user!'})
        return jsonify({'status' : True})
    else:
        # return jsonify({'status' : 'Failed to create user'})
        return jsonify({'status' : False})

### LOGIN USER
@users_api_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.get(User.username == username)

    result = jsonify({
        'status' : True,
        'data' : user.as_json_dict()
    })

    if not user:
        # return jsonify({'status' : 'Incorrect username or password'})
        return jsonify({'status' : False})
    else:
        if password == user.password:
            login_user(user)
            return result
        else:
            return jsonify({'status' : False})

### LOGOUT USER
@users_api_blueprint.route('/logout')
def logout():
    logout_user()
    return jsonify({'status' : True})

### SHOW TRIPS
@users_api_blueprint.route('/<id>/trips', methods=['GET'])
def get_trips(id):
    trip = Trip.select().where(Trip.parent_user_id==id)
    trip_list = []
    for t in trip:
        trip_list.append( t.as_json_dict() )

    result = jsonify( {
        'data': jsonify(trip_list)
    } )
    return result

