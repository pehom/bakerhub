# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.customer import Customer  # noqa: E501
from swagger_server.models.customer_review import CustomerReview  # noqa: E501
from swagger_server.models.default_error import DefaultError  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCustomersController(BaseTestCase):
    """CustomersController integration test stubs"""

    def test_create_customer(self):
        """Test case for create_customer

        Creats new customer
        """
        body = Customer()
        response = self.client.open(
            '/v1/customers',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_customer_review(self):
        """Test case for create_customer_review

        Creates customer review
        """
        body = CustomerReview()
        response = self.client.open(
            '/v1/customers/{customer_id}/reviews'.format(customer_id='customer_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_customer_review_by_id(self):
        """Test case for delete_customer_review_by_id

        Deletes customer review
        """
        query_string = [('review_id', 'review_id_example')]
        response = self.client.open(
            '/v1/customers/{customer_id}/reviews'.format(customer_id='customer_id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_customer_by_id(self):
        """Test case for get_customer_by_id

        Returns customer with requested Id
        """
        response = self.client.open(
            '/v1/customers/{customer_id}'.format(customer_id='customer_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_customer_reviews_by_customer_id(self):
        """Test case for get_customer_reviews_by_customer_id

        Returns customer reviews
        """
        response = self.client.open(
            '/v1/customers/{customer_id}/reviews'.format(customer_id='customer_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_customers(self):
        """Test case for get_customers

        Returns customers
        """
        query_string = [('status', 'status_example')]
        response = self.client.open(
            '/v1/customers',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_customer_by_id(self):
        """Test case for update_customer_by_id

        Updates existing customer
        """
        body = Customer()
        response = self.client.open(
            '/v1/customers/{customer_id}'.format(customer_id='customer_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
