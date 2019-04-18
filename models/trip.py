from models.base_model import BaseModel
import peewee as pw
from models.user import User
from Travola_API.utils.AWSHelper import S3_LOCATION

class Trip(BaseModel):
    parent_user = pw.ForeignKeyField(User, backref='trips', unique=False, on_delete='CASCADE', index=True)
    trip_name = pw.CharField(unique=False, null=False)
    trip_img_url = pw.TextField(unique=False, null=True)
    trip_desc = pw.TextField(unique=False, null=True)
    
    def as_dict(self):
        json_dict = {
            'id' : self.id,
            'parent_user' : self.parent_user.id,
            'trip_name' : self.trip_name,
            'trip_img_url' : self.trip_img_url,
            'trip_desc' : self.trip_desc
        }
        return json_dict
    
    def s3_img_url(self):
        return S3_LOCATION + "trip_display_imgs/" + self.trip_img_url