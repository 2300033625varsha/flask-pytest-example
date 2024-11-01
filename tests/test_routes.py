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
        
        # Create test products
        cls.product1 = Product(name='Product One', price=10.99, description='First test product.', category='Category A')
        cls.product2 = Product(name='Product Two', price=20.99, description='Second test product.', category='Category B')
        
        db_session.add(cls.product1)
        db_session.add(cls.product2)
        db_session.commit()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests are done."""
        db_session.delete(cls.product1)
        db_session.delete(cls.product2)
        db_session.commit()

    def test_list_all_products(self):
        """Test listing all products."""
        response = self.client.get('/products')  # Assuming this is your endpoint
        self.assertEqual(response.status_code, 200)  # Check that the response code is 200
        
        data = response.get_json()
        self.assertIsInstance(data, list)  # Ensure the response data is a list
        self.assertEqual(len(data), 2)  # Check that we have two products in the list
        
        # Check that the products in the response match the expected products
        product_names = [product['name'] for product in data]
        self.assertIn('Product One', product_names)  # Check for the first product
        self.assertIn('Product Two', product_names)  # Check for the second product

    def test_list_all_products_empty(self):
        """Test listing all products when there are none."""
        # Remove all products for this test
        db_session.delete(self.product1)
        db_session.delete(self.product2)
        db_session.commit()

        response = self.client.get('/products')  # Assuming this is your endpoint
        self.assertEqual(response.status_code, 200)  # Check that the response code is 200
        
        data = response.get_json()
        self.assertIsInstance(data, list)  # Ensure the response data is a list
        self.assertEqual(len(data), 0)  # Check that the list is empty

if __name__ == '__main__':
    unittest.main()
