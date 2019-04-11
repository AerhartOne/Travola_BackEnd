from models.base_model import BaseModel
from models.user import User
from models.trip import Trip
import peewee as pw

class UserTrip(BaseModel):
    user = pw.ForeignKeyField(User, backref="users")
    trip = pw.ForeignKeyField(Trip, backref="trips")