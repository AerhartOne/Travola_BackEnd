from models.base_model import BaseModel
import peewee as pw
from models.trip import Trip

class TripEvent(BaseModel):
    parent_trip_id = pw.ForeignKeyField(Trip, backref='tripevent', unique=False, on_delete='CASCADE')
    date_time = pw.DateTimeField()
    location = pw.CharField(unique=False)