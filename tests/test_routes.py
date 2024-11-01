import unittest
from your_app import create_app  # Adjust import based on your app structure
from your_app.database import db_session
from your_app.models import Product

class TestProductRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a test client and test product before running the tests."""
        cls.app = create_app()
        cls.client = cls.app.test_client()
        
        cls.product = Product(name='Old Product', price=29.99, description='An old product.', category='Old Category')
        db_session.add(cls.product)
        db_session.commit()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests are done."""
        db_session.delete(cls.product)
        db_session.commit()

    def test_update_product(self):
        """Test updating a product."""
        updated_data = {
            'name': 'Updated Product',
            'price': 39.99,
            'description': 'An updated product.',
            'category': 'Updated Category'
        }
        
        response = self.client.put(f'/products/{self.product.id}', json=updated_data)  # Assuming this is your endpoint
        self.assertEqual(response.status_code, 200)  # Check that the response code is 200
        
        # Verify that the product was updated
        updated_product = db_session.query(Product).get(self.product.id)
        self.assertEqual(updated_product.name, 'Updated Product')  # Check updated name
        self.assertEqual(updated_product.price, 39.99)  # Check updated price
        self.assertEqual(updated_product.description, 'An updated product.')  # Check updated description
        self.assertEqual(updated_product.category, 'Updated Category')  # Check updated category

    def test_update_nonexistent_product(self):
        """Test updating a product that does not exist."""
        updated_data = {
            'name': 'Nonexistent Product',
            'price': 49.99,
            'description': 'This product does not exist.',
            'category': 'Nonexistent Category'
        }
        
        response = self.client.put('/products/9999', json=updated_data)  # Using an ID that does not exist
        self.assertEqual(response.status_code, 404)  # Check that the response code is 404

if __name__ == '__main__':
    unittest.main()
