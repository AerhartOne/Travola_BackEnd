from models.base_model import BaseModel
import peewee as pw

class UserTrip(BaseModel):
    user = pw.ForeignKeyField(User, backref="users")
    trip = pw.ForeignKeyField(Trip, backref="trips")