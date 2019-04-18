from models.base_model import BaseModel
import peewee as pw
from models.trip import Trip

class TripEvent(BaseModel):
    parent_trip = pw.ForeignKeyField(Trip, backref='trip_events', unique=False, on_delete='CASCADE')
    date_time = pw.DateTimeField(unique=False, null=False)
    location = pw.CharField(unique=False, null=True)
    desc = pw.TextField(unique=False, null=True)

    def as_dict(self):
        json_dict = {
            'id': self.id,
            'parent_trip': self.parent_trip.id,
            'date_time': self.date_time,
            'location': self.location,
            'desc': self.desc
        }
        return json_dict