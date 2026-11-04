import unittest
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_greetings_page(self):
        response = self.client.get("/hi/John?age=30")
        self.assertEqual(response.status_code, 200)

    def test_admin_page(self):
        response = self.client.get("/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)