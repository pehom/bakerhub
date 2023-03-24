# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.default_error import DefaultError  # noqa: E501
from swagger_server.models.product import Product  # noqa: E501
from swagger_server.models.product_review import ProductReview  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProductsController(BaseTestCase):
    """ProductsController integration test stubs"""

    def test_create_product(self):
        """Test case for create_product

        Creats a new product
        """
        body = Product()
        response = self.client.open(
            '/v1/products',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_product_review(self):
        """Test case for create_product_review

        Creates product review
        """
        body = ProductReview()
        response = self.client.open(
            '/v1/products/{product_id}/reviews'.format(product_id='product_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_product_by_id(self):
        """Test case for delete_product_by_id

        
        """
        response = self.client.open(
            '/v1/products/{product_id}'.format(product_id='product_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_product_review_by_id(self):
        """Test case for delete_product_review_by_id

        Deletes product review
        """
        query_string = [('review_id', 'review_id_example')]
        response = self.client.open(
            '/v1/products/{product_id}/reviews'.format(product_id='product_id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_product_by_id(self):
        """Test case for get_product_by_id

        Returns product with requested ID
        """
        response = self.client.open(
            '/v1/products/{product_id}'.format(product_id='product_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_product_reviews_by_product_id(self):
        """Test case for get_product_reviews_by_product_id

        Returns product reviews
        """
        response = self.client.open(
            '/v1/products/{product_id}/reviews'.format(product_id='product_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_products(self):
        """Test case for get_products

        Returns products of all bakers
        """
        query_string = [('title', 'title_example'),
                        ('baker_id', 'baker_id_example'),
                        ('rating', 1.2)]
        response = self.client.open(
            '/v1/products',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_product_by_id(self):
        """Test case for update_product_by_id

        Updating existing product
        """
        body = Product()
        response = self.client.open(
            '/v1/products/{product_id}'.format(product_id='product_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
