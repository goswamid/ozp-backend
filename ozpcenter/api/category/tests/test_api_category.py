"""
Tests for category endpoints
"""
import unittest

from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from ozpcenter.scripts import sample_data_generator as data_gen
import ozpcenter.api.category.views as views
from ozpcenter import models as models
from ozpcenter import model_access as generic_model_access


class CategoryApiTest(APITestCase):

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

    def test_get_categories_list(self):
        user = generic_model_access.get_profile('wsmith').user
        self.client.force_authenticate(user=user)
        url = '/api/category/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [i['title'] for i in response.data]
        self.assertTrue('Business' in titles)
        self.assertTrue('Education' in titles)
        self.assertTrue(len(titles) > 5)

    def test_get_category(self):
        user = generic_model_access.get_profile('wsmith').user
        self.client.force_authenticate(user=user)
        url = '/api/category/1/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        title = response.data['title']
        description = response.data['description']
        self.assertEqual(title, 'Books and Reference')
        self.assertTrue(description != None)

    def test_create_category(self):
        user = generic_model_access.get_profile('bigbrother').user
        self.client.force_authenticate(user=user)
        url = '/api/category/'
        data = {'title': 'new category', 'description': 'category description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        title = response.data['title']
        description = response.data['description']
        self.assertEqual(title, 'new category')
        self.assertEqual(description, 'category description')

    def test_update_category(self):
        user = generic_model_access.get_profile('bigbrother').user
        self.client.force_authenticate(user=user)
        url = '/api/category/1/'
        data = {'title': 'updated category', 'description': 'updated description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        title = response.data['title']
        description = response.data['description']
        self.assertEqual(title, 'updated category')
        self.assertEqual(description, 'updated description')

    def test_delete_category(self):
        user = generic_model_access.get_profile('bigbrother').user
        self.client.force_authenticate(user=user)
        url = '/api/category/1/'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

