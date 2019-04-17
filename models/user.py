from models.base_model import BaseModel
from flask_login import UserMixin
import peewee as pw
from app import app

### USER MODEL
class User(UserMixin, BaseModel):
    username = pw.CharField(unique=True, index=True)
    password = pw.CharField(index=True)
    email = pw.CharField(unique=True, index=True)
    first_name = pw.CharField(unique=False, null=False)
    last_name = pw.CharField(unique=False, null=False)
    bio_text = pw.TextField(unique=False, null=True)
    avatar_url = pw.TextField(unique=False, null=True)

    def validate(self):
        if len(self.password) < 6:
            self.errors.append("Password must be at least 6 characters!")
        if len(self.username) < 5:
            self.errors.append('Username must be at least 5 characteers long!')
        if not self.password:
            self.errors.append('You must enter a password!')

    def as_dict(self):
        json_dict = {
            'id' : self.id,
            'username' : self.username,
            'email' : self.email,
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'bio_text' : self.bio_text,
            'avatar_url' : self.avatar_url
        }
        return json_dict