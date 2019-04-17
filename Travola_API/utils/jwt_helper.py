from app import app
from flask_jwt import JWT
from models.user import User
import os

def authenticate(username, password):
    selected_user = User.get_or_none(User.username == username)
    if selected_user and (selected_user.password == password):
        return selected_user.as_dict()

def identity(payload):
    user_id = payload['identity']
    selected_user = User.get_or_none(User.id == user_id)
    if selected_user:
        return selected_user.as_dict()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWT(app, authenticate, identity)