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
        cls.product1 = Product(name='Product One', price=10.99, description='First test product.', category='Category A', available=True)
        cls.product2 = Product(name='Product Two', price=20.99, description='Second test product.', category='Category B', available=False)
        cls.product3 = Product(name='Product Three', price=15.99, description='Third test product.', category='Category A', available=True)
        
        db_session.add(cls.product1)
        db_session.add(cls.product2)
        db_session.add(cls.product3)
        db_session.commit()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests are done."""
        db_session.delete(cls.product1)
        db_session.delete(cls.product2)
        db_session.delete(cls.product3)
        db_session.commit()

    def test_list_by_availability(self):
        """Test listing products by availability."""
        response = self.client.get('/products?available=true')  # Assuming this is your endpoint
        self.assertEqual(response.status_code, 200)  # Check that the response code is 200
        
        data = response.get_json()
        self.assertIsInstance(data, list)  # Ensure the response data is a list
        self.assertEqual(len(data), 2)  # Check that we have two available products
        
        # Check that the returned products are available
        for product in data:
            self.assertTrue(product['available'])

    def test_list_by_availability_no_results(self):
        """Test listing products by availability when there are none."""
        response = self.client.get('/products?available=false')  # Querying availability status that does not exist
        self.assertEqual(response.status_code, 200)  # Check that the response code is 200
        
        data = response.get_json()
        self.assertIsInstance(data, list)  # Ensure the response data is a list
        self.assertEqual(len(data), 1)  # Check that the list has one product that is not available

        # Check that the returned product is not available
        for product in data:
            self.assertFalse(product['available'])

if __name__ == '__main__':
    unittest.main()
