import connexion
import six

from paymentprovider.models.error import Error  # noqa: E501
from paymentprovider.models.payment_creation_response import PaymentCreationResponse  # noqa: E501
from paymentprovider.models.payment_data import PaymentData  # noqa: E501
from paymentprovider.models.payment_request import PaymentRequest  # noqa: E501
from paymentprovider import util
from redis import Redis
import requests
import json
import uuid
import time
import logging
from os import environ
from luhn import verify as verifyluhn


""" This dictionary simulates a key-value database where:
    - the Key is the payment receiver 
    - the Value is the URL where PaymentProvider will post the payment result
    It could have been done on Redis but, just for the sake of simplicity, it is stored here.
"""
served_company = {
    "ACMESky": "http://acmesky_backend:8080/payments",
}


def create_payment_request(payment_request=None):  # noqa: E501
    """createPaymentRequest

    Creates a payment request for a user. API for: ACMESky # noqa: E501

    :param payment_request: 
    :type payment_request: dict | bytes

    :rtype: PaymentCreationResponse
    """
    if connexion.request.is_json:
        payment_request = PaymentRequest.from_dict(connexion.request.get_json())  # noqa: E501
    
    # This line simulates a network slowdown (comment if not needed).
    time.sleep(5)

    """ Generate an unique transaction id and associate the id with the payment request
    """
    transaction_id = str(uuid.uuid1())
    redis_connection = Redis(host="payment_provider_redis", port=6379, db=0)
    redis_connection.set(transaction_id, json.dumps(payment_request.to_dict()))
    redis_connection.close()

    """ Return the url where the user can pay
    """
    frontend_url = environ.get("PAYMENT_PROVIDER_FRONTEND", "http://0.0.0.0:4002")
    redirect_page = f'{frontend_url}/?transaction_id={transaction_id}'  # The transaction id will be used to retrieve the informations saved on redis
    return PaymentCreationResponse(redirect_page=redirect_page, transaction_id=transaction_id)


def get_payment_details(transaction_id):  # noqa: E501
    """Your GET endpoint

    Gets the information for the payment request for a user. API for: User # noqa: E501

    :param transaction_id: ID of transaction
    :type transaction_id: 

    :rtype: PaymentRequest
    """
    redis_connection = Redis(host="payment_provider_redis", port=6379, db=0)
    payment_request = json.loads(redis_connection.get(transaction_id))
    redis_connection.close()
    return PaymentRequest.from_dict(payment_request)


def send_payment(payment_data=None):  # noqa: E501
    """sendPayment

    Sends the payment data for paying a request. API for: User # noqa: E501

    :param payment_data: 
    :type payment_data: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payment_data = PaymentData.from_dict(connexion.request.get_json())  # noqa: E501

    # Simulate the time spent to communicate with the bank
    time.sleep(1)

    """ Send the payment status to ACMESky Backend 
        If the cvv is 456 or the credit card number is not valid the payment status will be false
    """
    status = True if payment_data.cvv != "456" and verifyluhn(payment_data.credit_cart_number) else False
    payment_information = {
        'transaction_id': payment_data.transaction_id,
        'status': status
    }

    """ Retrieve the payment request data for the company name from Redis
    """
    redis_connection = Redis(host="payment_provider_redis", port=6379, db=0)
    payment_request = json.loads(redis_connection.get(payment_data.transaction_id))
    redis_connection.close()

    payment_receiver_url = served_company[payment_request["payment_receiver"]]

    requests.post(payment_receiver_url, json=payment_information)
    return ("", 200) if status else ("", 400)
