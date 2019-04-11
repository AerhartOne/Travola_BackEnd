from models.base_model import BaseModel
import peewee as pw

class PhotoAttachment(BaseModel):
    parent_event = pw.ForeignKeyField(Event, backref="events")
    url = pw.TextField(null=True)