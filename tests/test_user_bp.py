import unittest
from app import create_app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_greetings_page(self):
        response = self.client.get("/hi/John?age=30")
        self.assertEqual(response.status_code, 200)

    def test_admin_page(self):
        response = self.client.get("/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)