from models.base_model import BaseModel
import peewee as pw
from models.payment import Payment
from models.user import User

class Subscription(BaseModel):
    for_user = pw.ForeignKeyField(User, backref="subscriptions")
    payment = pw.ForeignKeyField(Payment, backref="subscriptions")

    def as_dict(self):
        json_dict = {
            'id' : self.id,
            'for_user' : self.for_user,
            'payment' : self.payment,
        }
        return json_dict