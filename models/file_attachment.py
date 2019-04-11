from models.base_model import BaseModel
from models.trip_event import TripEvent
import peewee as pw

class FileAttachment(BaseModel):
    parent_event = pw.ForeignKeyField(TripEvent, backref="events")
    url = pw.TextField(null=True)

    def as_json_dict(self):
        json_dict = {
            'parent_event': self.parent_event.id,
            'url': self.url
        }
        return json_dict
    