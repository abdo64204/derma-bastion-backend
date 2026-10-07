from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import ContactMessage


class ContactAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_submit_contact_message(self):
        payload = {
            "name": "Sarah Hassan",
            "email": "sarah@example.com",
            "phone": "01234567890",
            "subject": "Question about Hyaluronic Serum",
            "message": "Is this product suitable for sensitive skin?"
        }
        response = self.client.post('/api/contact/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ContactMessage.objects.filter(name="Sarah Hassan").exists())
