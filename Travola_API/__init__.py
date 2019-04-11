from app import app
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from Travola_API.blueprints.users.views import users_api_blueprint
from Travola_API.blueprints.trips.views import trips_api_blueprint
from Travola_API.blueprints.trip_events.views import trip_event_api_blueprint 
from Travola_API.blueprints.file_attachments.views import file_attachments_api_blueprint
from Travola_API.blueprints.photo_attachments.views import photo_attachments_api_blueprint

app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(trips_api_blueprint, url_prefix='/api/v1/trips')
app.register_blueprint(trip_event_api_blueprint, url_prefix='/api/v1/trip_events')
app.register_blueprint(file_attachments_api_blueprint, url_prefix='/api/v1/file_attachments')
app.register_blueprint(photo_attachments_api_blueprint, url_prefix='/api/v1/photo_attachments')