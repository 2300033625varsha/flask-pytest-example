
import unittest
from your_app import create_app  # Adjust import based on your app structure
from your_app.database import db_session
from your_app.models import Product

class TestProductRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a test client and test products before running the tests."""
        cls.app = create_app()
        cls.client = cls.app.test_client()
        
        cls.product = Product(name='Test Product', price=19.99, description='A test product.', category='Test Category')
        db_session.add(cls.product)
        db_session.commit()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests are done."""
        db_session.delete(cls.product)
        db_session.commit()

    def test_read_product(self):
        """Test reading a product by ID."""
        response = self.client.get(f'/products/{self.product.id}')  # Assuming this is your endpoint
        self.assertEqual(response.status_code, 200)  # Check that the response code is 200
        
        data = response.get_json()
        self.assertIsNotNone(data)  # Ensure we received some data
        self.assertEqual(data['name'], 'Test Product')  # Check that the product name matches
        self.assertEqual(data['price'], 19.99)  # Check that the product price matches
        self.assertEqual(data['description'], 'A test product.')  # Check description
        self.assertEqual(data['category'], 'Test Category')  # Check category

    def test_read_nonexistent_product(self):
        """Test reading a product that does not exist."""
        response = self.client.get('/products/9999')  # Using an ID that does not exist
        self.assertEqual(response.status_code, 404)  # Check that the response code is 404

if __name__ == '__main__':
    unittest.main()
