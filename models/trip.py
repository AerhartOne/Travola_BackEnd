from models.base_model import BaseModel
import peewee as pw
from models.user import User

class Trip(BaseModel):
    parent_user = pw.ForeignKeyField(User, backref='trips', unique=False, on_delete='CASCADE', index=True)
    trip_name = pw.CharField(unique=False, null=False)
    trip_img_url = pw.TextField(unique=False, null=True)

    
    def as_dict(self):
        json_dict = {
            'id' : self.id,
            'parent_user' : self.parent_user.id,
            'trip_name' : self.trip_name,
            'trip_img_url' : self.trip_img_url
        }
        return json_dict
    