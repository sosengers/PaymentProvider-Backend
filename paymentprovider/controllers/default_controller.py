import connexion
import six

from paymentprovider.models.error import Error  # noqa: E501
from paymentprovider.models.payment_creation_response import PaymentCreationResponse  # noqa: E501
from paymentprovider.models.payment_data import PaymentData  # noqa: E501
from paymentprovider.models.payment_request import PaymentRequest  # noqa: E501
from paymentprovider import util


def create_payment_request(payment_request=None):  # noqa: E501
    """createPaymentRequest

    Creates a payment request for a user. API for: ACMESky # noqa: E501

    :param payment_request: 
    :type payment_request: dict | bytes

    :rtype: PaymentCreationResponse
    """
    if connexion.request.is_json:
        payment_request = PaymentRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def send_payment(payment_data=None):  # noqa: E501
    """sendPayment

    Sends the payment data for paying a request. API for: User # noqa: E501

    :param payment_data: 
    :type payment_data: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payment_data = PaymentData.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
