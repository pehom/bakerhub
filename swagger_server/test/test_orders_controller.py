# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.default_error import DefaultError  # noqa: E501
from swagger_server.models.order import Order  # noqa: E501
from swagger_server.test import BaseTestCase


class TestOrdersController(BaseTestCase):
    """OrdersController integration test stubs"""

    def test_create_order(self):
        """Test case for create_order

        Creats new order
        """
        body = Order()
        response = self.client.open(
            '/v1/orders',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_order_by_id(self):
        """Test case for get_order_by_id

        Returns order with requested ID
        """
        response = self.client.open(
            '/v1/orders/{order_id}'.format(order_id='order_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_orders(self):
        """Test case for get_orders

        Returns orders
        """
        query_string = [('status', 'status_example'),
                        ('customer_id', 'customer_id_example'),
                        ('baker_id', 'baker_id_example')]
        response = self.client.open(
            '/v1/orders',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_order_by_id(self):
        """Test case for update_order_by_id

        Updates existing order
        """
        body = Order()
        response = self.client.open(
            '/v1/orders/{order_id}'.format(order_id='order_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
