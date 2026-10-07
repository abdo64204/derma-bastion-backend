from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import StoreSettings


class StoreSettingsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_store_config(self):
        response = self.client.get('/api/store-config/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('vodafoneCash', response.data)
        self.assertIn('instapay', response.data)
        self.assertIn('cardGateway', response.data)
        self.assertIn('shipping', response.data)
        self.assertEqual(response.data['shipping']['freeShippingFrom'], 1500.0)
        self.assertEqual(response.data['shipping']['shippingFee'], 60.0)
