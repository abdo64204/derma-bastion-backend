from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Product
from .models import Order


class OrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(
            id=1,
            name="Hyaluronic Acid Serum 30ml",
            category="Skin Care",
            price=550.00,
        )

    def test_create_order_cod(self):
        payload = {
            "delivery": {
                "fullName": "Ahmed Mohamed",
                "phone": "01012345678",
                "governorate": "Cairo",
                "city": "Nasr City",
                "address": "15 Abbas El Akkad, Floor 4",
                "notes": "Call before arriving"
            },
            "items": [
                {
                    "product": {
                        "id": self.product.id,
                        "name": self.product.name,
                        "category": self.product.category,
                        "price": float(self.product.price)
                    },
                    "quantity": 2
                }
            ],
            "subtotal": 1100.0,
            "shipping": 60.0,
            "total": 1160.0,
            "payment": {
                "method": "cod",
                "status": "paid_on_delivery"
            }
        }

        response = self.client.post('/api/orders/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['id'].startswith('DB-'))
        self.assertEqual(response.data['total'], 1160.0)
        self.assertEqual(response.data['delivery']['fullName'], "Ahmed Mohamed")
        self.assertEqual(response.data['status'], 'placed')
        self.assertEqual(len(response.data['items']), 1)

    def test_invalid_egyptian_phone(self):
        payload = {
            "delivery": {
                "fullName": "Ahmed Mohamed",
                "phone": "12345",  # Invalid!
                "governorate": "Cairo",
                "city": "Nasr City",
                "address": "15 Abbas El Akkad, Floor 4",
                "notes": ""
            },
            "items": [
                {
                    "product": {"id": self.product.id, "name": self.product.name, "price": 550.0},
                    "quantity": 1
                }
            ],
            "subtotal": 550.0,
            "shipping": 60.0,
            "total": 610.0,
            "payment": {
                "method": "cod",
                "status": "paid_on_delivery"
            }
        }

        response = self.client.post('/api/orders/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('delivery', response.data)
        self.assertIn('phone', response.data['delivery'])

    def test_track_order(self):
        order = Order.objects.create(
            id="DB-999888",
            full_name="Fatima Ali",
            phone="01123456789",
            governorate="Alexandria",
            city="Smouha",
            address="Fouad Street Building 10",
            subtotal=550.0,
            shipping=0.0,
            total=550.0,
            payment_method="cod",
            payment_status="paid_on_delivery",
            status="confirmed"
        )

        response = self.client.get(f'/api/orders/{order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], "DB-999888")
        self.assertEqual(response.data['timeline']['currentStepIndex'], 1)

        # Query param tracking endpoint
        track_resp = self.client.get('/api/orders/track/?order=DB-999888')
        self.assertEqual(track_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(track_resp.data['id'], "DB-999888")
