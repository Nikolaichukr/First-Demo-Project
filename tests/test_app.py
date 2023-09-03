import unittest
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Quote of the Day', response.data)

    def test_quote_display(self):
        response = self.client.get('/')
        self.assertIn(b'<blockquote>', response.data)
        self.assertIn(b'</blockquote>', response.data)


if __name__ == '__main__':
    unittest.main()
