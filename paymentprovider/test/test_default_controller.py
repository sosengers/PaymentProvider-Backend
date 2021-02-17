# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from paymentprovider.models.error import Error  # noqa: E501
from paymentprovider.models.payment_data import PaymentData  # noqa: E501
from paymentprovider.models.payment_request import PaymentRequest  # noqa: E501
from paymentprovider.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_create_payment_request(self):
        """Test case for create_payment_request

        createPaymentRequest
        """
        payment_request = {
  "transaction_id" : "046b6c7f-0b8a-43b9-b35d-6489e6daee91",
  "amount" : 0.08008281904610115,
  "description" : "description",
  "payment_receiver" : "payment_receiver"
}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/payments/request',
            method='POST',
            headers=headers,
            data=json.dumps(payment_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_send_payment(self):
        """Test case for send_payment

        sendPayment
        """
        payment_data = {
  "transaction_id" : "046b6c7f-0b8a-43b9-b35d-6489e6daee91",
  "credit_cart_number" : "credit_cart_number",
  "cvv" : "cvv",
  "owner_name" : "owner_name",
  "expiration_date" : "2000-01-23"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/payments/pay',
            method='POST',
            headers=headers,
            data=json.dumps(payment_data),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
