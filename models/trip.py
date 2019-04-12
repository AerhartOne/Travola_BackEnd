from models.base_model import BaseModel
import peewee as pw
from models.user import User

class Trip(BaseModel):
    trip_name = pw.CharField(unique=False, null=False)
    parent_user = pw.ForeignKeyField(User, backref='trips', unique=False, on_delete='CASCADE', index=True)