from flask import Blueprint, request, flash
from datetime import datetime
from datetime import date
from models.user import User
from models.trip import Trip
from models.subscription import Subscription
from flask.json import jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import Travola_API.utils.jwt_helper
from flask_jwt_extended import jwt_required, current_user
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
        password = hashed_password,
        bio_text = ''
        )
    new_user.save()

    successfully_created = (User.get_or_none( User.username ==  new_user.username ) != None)

    result = jsonify({
        'status' : successfully_created,
        'data' : new_user.as_dict()
    })
    return result

@users_api_blueprint.route('/edit', methods=['POST'])
@jwt_required
def edit():
    received_data = request.form
    target_user = User.get_or_none( User.id==received_data['user_id'] )

    target_user.username = received_data['username']
    target_user.email = received_data['email']
    target_user.first_name = received_data['first_name']
    target_user.last_name = received_data['last_name']
    target_user.bio_text = received_data['bio_text']

    if (received_data['password'] != ''):
        hashed_password = generate_password_hash(received_data['password'])
        target_user.password = hashed_password

    if target_user.save():
        successfully_edited = True

    result = jsonify({
        'status' : successfully_edited,
        'data' : target_user.as_dict()
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

    return_data = None

    if user_found:
        if check_password_hash(user_object.password, password):
            access_token = create_access_token(identity=user_object.as_dict())
            refresh_token = create_refresh_token(identity=user_object.as_dict())
            return_data = user_object.as_dict()
            logged_in = True
        else:
            user_object = None



    result = jsonify({
        'status' : (user_found and logged_in),
        'data' : return_data,
        'access_token' : access_token,
        'refresh_token' : refresh_token
    })
    return result

### LOGOUT USER
@users_api_blueprint.route('/logout')
def logout():
    return jsonify({
        'status' : True
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
