from models.base_model import BaseModel
from models.trip_event import TripEvent
import peewee as pw

class FileAttachment(BaseModel):
    parent_event = pw.ForeignKeyField(TripEvent, backref="events")
    url = pw.TextField(null=True)
    