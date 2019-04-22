from models.base_model import BaseModel
from models.trip_event import TripEvent
import peewee as pw
from app import app

class PhotoAttachment(BaseModel):
    parent_event = pw.ForeignKeyField(TripEvent, backref="photo_attachments", on_delete='CASCADE')
    url = pw.TextField(null=True)
    title = pw.CharField(null=True, default='Unnamed Photo')

    def as_dict(self):
        json_dict = {
            'parent_event': self.parent_event.id,
            'title': self.title,
            'url': self.url,
            's3_url': self.s3_url()
        }
        return json_dict

    def s3_url(self):
        return app.config['S3_LOCATION'] + "photos/" + self.url