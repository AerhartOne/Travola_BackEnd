from models.base_model import BaseModel
import peewee as pw

class Subscription(BaseModel):
    for_user = pw.ForeignKeyField(User, backref="users")
    payment = pw.ForeignKeyField(Payment, backref="payments")