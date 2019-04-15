from models.user import User
from models.trip import Trip
from models.trip_event import TripEvent
from models.file_attachment import FileAttachment
from models.photo_attachment import PhotoAttachment

User.delete().execute()
Trip.delete().execute()
TripEvent.delete().execute()
FileAttachment.delete().execute()
PhotoAttachment.delete().execute()