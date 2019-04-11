import os
import config
from flask import Flask
from models.base_model import db
from flask_wtf.csrf import CSRFProtect
import flask_login 

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('Travola', root_path=web_dir)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
csrf = CSRFProtect(app)

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