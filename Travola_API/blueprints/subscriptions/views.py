from flask import Blueprint, request
from flask.json import jsonify
from models.user import User
from models.subscription import Subscription
from models.payment import Payment
from Travola_API.utils.braintree_helper import generate_client_token, transact

subscriptions_api_blueprint = Blueprint('subscriptions_api',
                             __name__,
                             template_folder='templates')

@subscriptions_api_blueprint.route('/token', methods=['GET'])
def token():
    return generate_client_token()

@subscriptions_api_blueprint.route('/new', methods=['POST'])
def new():
    data = request.form
    subscription_amount = 5
    target_user = User.get_or_none( User.id == data['user_id'])
    payment_nonce = request.form['payment_method_nonce']
    payment_succeeded = False
    new_subscription = None

    if (target_user):
        transaction = transact( {
            "amount": subscription_amount,
            "payment_method_nonce": payment_nonce,
            "options": {
                "submit_for_settlement": True
            }
        } )
        
        print(transaction)
        if transaction:
            new_payment = Payment.create(
                amount=subscription_amount,
                payment_nonce=payment_nonce
            )

            new_subscription = Subscription.create(
                payment=new_payment.id,
                for_user=target_user.id
            )

            payment_succeeded = True
    
    return_data = None
    if new_subscription:
        return_data = new_subscription.as_dict()

    result = jsonify({
        'status' : payment_succeeded,
        'data' : return_data
    })

    return result
