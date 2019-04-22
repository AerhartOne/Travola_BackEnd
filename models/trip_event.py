from models.base_model import BaseModel
import peewee as pw
from models.trip import Trip

class TripEvent(BaseModel):
    parent_trip = pw.ForeignKeyField(Trip, backref='trip_events', unique=False, on_delete='CASCADE')
    event_name = pw.CharField(unique=False, null=False, default="Unnamed Event")
    date_time = pw.DateTimeField(unique=False, null=False)
    location = pw.CharField(unique=False, null=True)
    desc = pw.TextField(unique=False, null=True)
    notification_sent = pw.BooleanField(unique=False, null=False, default=False)

    def as_dict(self):
        date_time_split = str( self.date_time ).split()
        json_dict = {
            'id': self.id,
            'event_name': self.event_name,
            'parent_trip': self.parent_trip.id,
            'date_time': f'{date_time_split[0]}T{date_time_split[1]}',
            'location': self.location,
            'desc': self.desc,
            'notification_sent': self.notification_sent
        }
        return json_dict