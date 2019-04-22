from models.base_model import BaseModel
from models.trip_event import TripEvent
from app import app
import peewee as pw

class FileAttachment(BaseModel):
    parent_event = pw.ForeignKeyField(TripEvent, backref="file_attachments", on_delete='CASCADE')
    url = pw.TextField(null=True)
    title = pw.CharField(null=True, default='Unnamed File')

    def as_dict(self):
        json_dict = {
            'parent_event': self.parent_event.id,
            'title': self.title,
            'url': self.url,
            's3_url': self.s3_url()
        }
        return json_dict
    
    def s3_url(self):
        return app.config['S3_LOCATION'] + "files/" + self.url