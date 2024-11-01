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
        
        cls.product = Product(name='Product to Delete', price=15.99, description='A product to be deleted.', category='Delete Category')
        db_session.add(cls.product)
        db_session.commit()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests are done."""
        # Make sure the product is deleted after tests, if still present
        existing_product = db_session.query(Product).get(cls.product.id)
        if existing_product:
            db_session.delete(existing_product)
            db_session.commit()

    def test_delete_product(self):
        """Test deleting a product."""
        response = self.client.delete(f'/products/{self.product.id}')  # Assuming this is your endpoint
        self.assertEqual(response.status_code, 204)  # Check that the response code is 204 (No Content)
        
        # Verify that the product was deleted
        deleted_product = db_session.query(Product).get(self.product.id)
        self.assertIsNone(deleted_product)  # Ensure the product no longer exists

    def test_delete_nonexistent_product(self):
        """Test deleting a product that does not exist."""
        response = self.client.delete('/products/9999')  # Using an ID that does not exist
        self.assertEqual(response.status_code, 404)  # Check that the response code is 404

if __name__ == '__main__':
    unittest.main()
