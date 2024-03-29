"""
Tests for library endpoints (listings in a user's library)
"""
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from ozpcenter.scripts import sample_data_generator as data_gen
import ozpcenter.api.library.views as views
from ozpcenter import models as models
from ozpcenter import model_access as generic_model_access


class LibraryApiTest(APITestCase):

    def setUp(self):
        """
        setUp is invoked before each test method
        """
        self

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the whole TestCase (only run once for the TestCase)
        """
        data_gen.run()

    def test_get_library(self):
        user = generic_model_access.get_profile('wsmith').user
        self.client.force_authenticate(user=user)
        url = '/api/library/'
        response = self.client.get(url, format='json')
        # print('response.data: %s' % response.data)

    def test_create_library(self):
        """
        POST to /self/library
        """
        user = generic_model_access.get_profile('wsmith').user
        self.client.force_authenticate(user=user)
        url = '/api/self/library/'
        data = {'listing': {'id': '1'}, 'folder': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['listing']['id'], 1)

    def test_get_library_list(self):
        """
        GET /self/library
        """
        user = generic_model_access.get_profile('wsmith').user
        self.client.force_authenticate(user=user)
        url = '/api/self/library/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('listing', response.data[0])
        self.assertIn('id', response.data[0]['listing'])
        self.assertIn('title', response.data[0]['listing'])
        self.assertIn('unique_name', response.data[0]['listing'])
        self.assertIn('folder', response.data[0])

    def test_get_library_pk(self):
        """
        GET /self/library/1
        """
        user = generic_model_access.get_profile('wsmith').user
        self.client.force_authenticate(user=user)
        url = '/api/self/library/1/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('listing', response.data)
        self.assertIn('id', response.data['listing'])
        self.assertIn('title', response.data['listing'])
        self.assertIn('unique_name', response.data['listing'])
        self.assertIn('folder', response.data)

    def test_update_library(self):
        """
        PUT self/library/update_all
        """
        user = generic_model_access.get_profile('wsmith').user
        self.client.force_authenticate(user=user)
        url = '/api/self/library/'
        response = self.client.get(url, format='json')
        put_data = []
        for i in response.data:
            data = {'id': i['id'], 'folder': 'test',
                'listing': {'id': i['listing']['id']}}
            put_data.append(data)

        url = '/api/self/library/update_all/'
        response = self.client.put(url, put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


