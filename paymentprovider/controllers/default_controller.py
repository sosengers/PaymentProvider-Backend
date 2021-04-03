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

def create_payment_request(payment_request=None):  # noqa: E501
    """createPaymentRequest

    Creates a payment request for a user. API for: ACMESky # noqa: E501

    :param payment_request: 
    :type payment_request: dict | bytes

    :rtype: PaymentCreationResponse
    """
    if connexion.request.is_json:
        payment_request = PaymentRequest.from_dict(connexion.request.get_json())  # noqa: E501

    transaction_id = str(uuid.uuid1())
    redis_connection = Redis(host="payment_provider_redis", port=6379, db=0)

    redis_connection.set(transaction_id, json.dumps(payment_request.to_dict()))
    redis_connection.close()

    redirect_page = f'http://0.0.0.0:4002/?transaction_id={transaction_id}' # The transaction id will be used to retrieve the informations saved on redis
    return PaymentCreationResponse(redirect_page=redirect_page, transaction_id=transaction_id)

def get_payment_details(transaction_id):  # noqa: E501
    """Your GET endpoint

    Gets the information for the payment request for a user. API for: User # noqa: E501

    :param transaction_id: ID of transaction
    :type transaction_id: 

    :rtype: PaymentRequest
    """
processInstanceId    redis_connection = Redis(host="payment_provider_redis", port=6379, db=0)
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

    # Checking payment information with the bank
    time.sleep(1)
    """
    if payment_data.cvv == "456": # Errore nel pagamento (credito insufficiente)
        status = False
    else:
        status = True
    """
    status = True if payment_data.cvv != "456" else False
    payment_information = {
        'transaction_id': payment_data.transaction_id,
        'status': status
    }

    requests.post("http://acmesky_backend:8080/payments", json=payment_information)
    return ("", 200) if status else ("", 400)
