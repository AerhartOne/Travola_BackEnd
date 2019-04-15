from models.base_model import BaseModel
from flask_login import UserMixin
import peewee as pw
from app import app

### USER MODEL
class User(UserMixin, BaseModel):
    first_name = pw.CharField(unique=False, null=False)
    last_name = pw.CharField(unique=False, null=False)
    email = pw.CharField(unique=True, index=True)
    username = pw.CharField(unique=True, index=True)
    password = pw.CharField(index=True)

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
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'email' : self.email,
            'username' : self.username
        }
        return json_dict