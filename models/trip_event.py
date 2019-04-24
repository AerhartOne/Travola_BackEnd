from models.base_model import BaseModel
import peewee as pw
from models.trip import Trip
from decimal import Decimal

class TripEvent(BaseModel):
    parent_trip = pw.ForeignKeyField(Trip, backref='trip_events', unique=False, on_delete='CASCADE')
    event_name = pw.CharField(unique=False, null=False, default="Unnamed Event")
    date_time = pw.DateTimeField(unique=False, null=False)
    location_address = pw.CharField(unique=False, null=True, default='')
    desc = pw.TextField(unique=False, null=True)
    notification_sent = pw.BooleanField(unique=False, null=False, default=False)
    latitude = pw.DecimalField(unique=False, null=True, default=0)
    longitude = pw.DecimalField(unique=False, null=True, default=0)

    def as_dict(self):
        date_time_split = str( self.date_time ).split()
        date_time_local = self.date_time
        if (len(date_time_split) == 2):
            date_time_local = f'{date_time_split[0]}T{date_time_split[1]}'

        json_dict = {
            'id': self.id,
            'event_name': self.event_name,
            'parent_trip': self.parent_trip.id,
            'date_time': self.date_time,
            'date_time_local': date_time_local,
            'location_address': self.location_address,
            'desc': self.desc,
            'notification_sent': self.notification_sent,
            'latitude': float(self.latitude),
            'longitude': float(self.longitude)
        }
        return json_dict