import os
import config
from flask import Flask
from models.base_model import db
from flask_wtf.csrf import CSRFProtect
import flask_login 
from mapbox import Geocoder, Maps

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'Travola_API')

app = Flask('Travola', root_path=web_dir)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
# csrf = CSRFProtect(app)

maps = Maps()
geocoder = Geocoder(access_token = os.environ.get("MAPBOX_KEY"))

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

@app.before_request
def before_request():
    db.connect()

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

@app.after_request
def after_request(response):
    db.close()
    return response