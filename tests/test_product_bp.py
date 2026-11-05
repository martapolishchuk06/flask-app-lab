import unittest
from app import create_app
from app.products.db import get_db

class FlaskProductBpTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        db = get_db()
        table = db.table('products')
        if len(table.all()) == 0:
            table.insert({
                "id": 1,
                "name": "Laptop",
                "price": 1200.00,
                "category": "Електроніка",
                "quantity": 10,
                "content": "Потужний ноутбук",
                "image": "uploads/default.jpg",
                "created_at": "2025-01-01 12:00:00"
            })

    def tearDown(self):
        self.app_context.pop()

    def test_products_list_page(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Список товарів".encode('utf-8'), response.data)

    def test_detail_product_page(self):
        db = get_db()
        first_product = db.table('products').all()[0]
        response = self.client.get(f"/products/{first_product['id']}")
        self.assertEqual(response.status_code, 200)