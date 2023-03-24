# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.baker import Baker  # noqa: E501
from swagger_server.models.baker_review import BakerReview  # noqa: E501
from swagger_server.models.default_error import DefaultError  # noqa: E501
from swagger_server.test import BaseTestCase


class TestBakersController(BaseTestCase):
    """BakersController integration test stubs"""

    def test_create_baker(self):
        """Test case for create_baker

        Creates a new baker
        """
        body = Baker()
        response = self.client.open(
            '/v1/bakers',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_baker_review(self):
        """Test case for create_baker_review

        Creates baker review
        """
        body = BakerReview()
        response = self.client.open(
            '/v1/bakers/{baker_id}/reviews'.format(baker_id='baker_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_baker_by_id(self):
        """Test case for delete_baker_by_id

        
        """
        response = self.client.open(
            '/v1/bakers/{baker_id}'.format(baker_id='baker_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_baker_review_by_id(self):
        """Test case for delete_baker_review_by_id

        Deletes baker review
        """
        query_string = [('review_id', 'review_id_example')]
        response = self.client.open(
            '/v1/bakers/{baker_id}/reviews'.format(baker_id='baker_id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_baker_reviews_by_baker_id(self):
        """Test case for get_baker_reviews_by_baker_id

        Returns baker reviews
        """
        response = self.client.open(
            '/v1/bakers/{baker_id}/reviews'.format(baker_id='baker_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_bakerby_id(self):
        """Test case for get_bakerby_id

        Returns backer with requested ID
        """
        response = self.client.open(
            '/v1/bakers/{baker_id}'.format(baker_id='baker_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_bakers(self):
        """Test case for get_bakers

        Returns list of bakers
        """
        query_string = [('status', 'status_example'),
                        ('rating', 1.2)]
        response = self.client.open(
            '/v1/bakers',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_baker_by_id(self):
        """Test case for update_baker_by_id

        Updates existing baker
        """
        body = Baker()
        response = self.client.open(
            '/v1/bakers/{baker_id}'.format(baker_id='baker_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
