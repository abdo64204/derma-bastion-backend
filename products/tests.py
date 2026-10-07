from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product


class ProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.p1 = Product.objects.create(
            id=1,
            name="Hyaluronic Acid Serum 30ml",
            name_ar="سيروم حمض الهيالورونيك 30 مل",
            category="Skin Care",
            category_ar="العناية بالبشرة",
            price=550.00,
            badge="Best Seller",
            is_best_seller=True,
            description="Hydrating serum",
            how_to_use="Apply 2 drops",
            ingredients="Hyaluronic acid",
            benefits=["Hydrating", "Lightweight"]
        )
        self.p2 = Product.objects.create(
            id=2,
            name="Anti-Dandruff Shampoo 250ml",
            name_ar="شامبو مضاد للقشرة 250 مل",
            category="Hair Care",
            category_ar="العناية بالشعر",
            price=320.00,
            description="Anti dandruff hair care",
            how_to_use="Wash hair",
            ingredients="Zinc",
            benefits=["Clean scalp"]
        )

    def test_list_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Test schema matches frontend
        first = response.data[0]
        self.assertEqual(first['name'], "Hyaluronic Acid Serum 30ml")
        self.assertEqual(first['price'], 550.0)
        self.assertIn('howToUse', first)
        self.assertIn('ar', first)
        self.assertEqual(first['ar']['name'], "سيروم حمض الهيالورونيك 30 مل")

    def test_filter_category(self):
        response = self.client.get('/api/products/?category=skin')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], 1)

    def test_search_query(self):
        response = self.client.get('/api/products/?search=dandruff')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], 2)

    def test_sorting(self):
        response = self.client.get('/api/products/?sort=priceAsc')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 2)  # 320 is cheaper than 550

        response_desc = self.client.get('/api/products/?sort=priceDesc')
        self.assertEqual(response_desc.status_code, status.HTTP_200_OK)
        self.assertEqual(response_desc.data[0]['id'], 1)

    def test_best_sellers_endpoint(self):
        response = self.client.get('/api/products/best-sellers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], 1)

    def test_product_detail(self):
        response = self.client.get(f'/api/products/{self.p1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['name'], "Hyaluronic Acid Serum 30ml")
