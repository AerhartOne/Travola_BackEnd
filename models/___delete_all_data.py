from models.user import User
from models.trip import Trip
from models.trip_event import TripEvent
from models.file_attachment import FileAttachment
from models.photo_attachment import PhotoAttachment
from models.payment import Payment
from models.subscription import Subscription

FileAttachment.delete().execute()
PhotoAttachment.delete().execute()
Subscription.delete().execute()
Payment.delete().execute()
User.delete().execute()
Trip.delete().execute()
TripEvent.delete().execute()