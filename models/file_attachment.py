from models.base_model import BaseModel
from models.trip_event import TripEvent
import peewee as pw
from Travola_API.utils.AWSHelper import S3_LOCATION

class FileAttachment(BaseModel):
    parent_event = pw.ForeignKeyField(TripEvent, backref="file_attachments")
    url = pw.TextField(null=True)

    def as_dict(self):
        json_dict = {
            'parent_event': self.parent_event.id,
            'url': self.url,
            's3_url': self.s3_url()
        }
        return json_dict
    
    def s3_url(self):
        return S3_LOCATION + "files/" + self.filepath