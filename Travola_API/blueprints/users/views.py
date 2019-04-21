from flask import Blueprint, request, flash
from datetime import datetime
from datetime import date
from models.user import User
from models.trip import Trip
from models.subscription import Subscription
from flask.json import jsonify
from flask_login import login_user, logout_user, current_user
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import Travola_API.utils.jwt_helper
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    selected_users = User.select()
    result = jsonify({
        'data' : [u.as_dict() for u in selected_users]
    })
    return result

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
    hashed_password = generate_password_hash(request.form['password'])
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        email = request.form['email'] ,
        username = request.form['username'],
        password = hashed_password
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

    access_token = None
    refresh_token = None

    if user_object != None:
        if check_password_hash(user_object.password, password):
            logged_in = login_user(user_object)
            access_token = create_access_token(identity=user_object.as_dict())
            refresh_token = create_refresh_token(identity=user_object.as_dict())
        else:
            user_object = None

    result = jsonify({
        'status' : (user_found and logged_in),
        'data' : user_object.as_dict(),
        'access_token' : access_token,
        'refresh_token' : refresh_token
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

@users_api_blueprint.route('/<id>/subscriptions', methods=['GET'])
def subscriptions(id):
    subscriptions = Subscription.select().where(Subscription.for_user == id)
    subscription_list = []

    for s in subscriptions:
        if (datetime.now().timestamp() - s.created_at.timestamp() <= (60 * 60 * 24 * 30) ):
            subscription_list.append( s.as_dict() )

    subscription_active = ( len( subscription_list ) > 0 )

    result = jsonify({
        'data' : {
            'subscription_is_active' : subscription_active,
            'subscriptions' : subscription_list
        }
    })
    return result
