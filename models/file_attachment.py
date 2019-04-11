from models.base_model import BaseModel
import peewee as pw

class FileAttachment(BaseModel):
    parent_event = pw.ForeignKeyField(Event, backref="events")
    url = pw.TextField(null=True)
    