from models.base_model import BaseModel
import peewee as pw

class Payment(BaseModel):
    amount = pw.DecimalField()
    payment_nonce = pw.TextField()