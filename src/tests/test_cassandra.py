"""
Unit tests for Cassandra operations
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs: Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import pytest
import uuid
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.product import Product
from daos.product_dao import ProductDAO


class TestProductDAO:
    """Test suite for Product DAO operations with Cassandra"""

    @pytest.fixture
    def mock_cassandra_connection(self):
        """Mock Cassandra cluster and session"""
        mock_cluster = MagicMock()
        mock_session = MagicMock()
        return mock_cluster, mock_session

    @pytest.fixture
    def product_dao(self, mock_cassandra_connection):
        """Create ProductDAO with mocked Cassandra connection"""
        mock_cluster, mock_session = mock_cassandra_connection
        
        # Patch the database connection
        with patch('daos.product_dao.db.get_cassandra_connection', 
                   return_value=(mock_cluster, mock_session)):
            dao = ProductDAO()
            # Override with our mocks
            dao.session = mock_session
            dao.cluster = mock_cluster
            return dao

    def test_insert_product(self, product_dao, mock_cassandra_connection):
        """
        TEST 1: WRITE OPERATION
        
        Tests that a product is correctly inserted into Cassandra.
        Verifies:
        - The correct INSERT query is executed
        - All product fields are passed as parameters
        - The session.execute method is called exactly once
        """
        # Arrange - Create test data
        mock_cluster, mock_session = mock_cassandra_connection
        test_id = uuid.uuid4()
        test_product = Product(
            product_id=test_id,
            name="Test Laptop",
            sku="LAP-TEST-001",
            price=1299.99
        )

        # Act - Insert the product
        product_dao.insert(test_product)

        # Assert - Verify the database interaction
        # Check that execute was called
        assert mock_session.execute.call_count == 1, \
            "session.execute should be called exactly once"
        
        # Get the arguments passed to execute
        call_args = mock_session.execute.call_args[0]
        query = call_args[0]
        params = call_args[1]
        
        # Verify the query structure
        assert "INSERT INTO" in query.upper(), \
            "Query should be an INSERT statement"
        assert "store_manager.products" in query, \
            "Query should target store_manager.products table"
        assert "id" in query and "name" in query and "sku" in query and "price" in query, \
            "Query should include all product fields"
        
        # Verify the parameters
        assert params[0] == test_id, "First parameter should be product ID"
        assert params[1] == "Test Laptop", "Second parameter should be product name"
        assert params[2] == "LAP-TEST-001", "Third parameter should be product SKU"
        assert params[3] == 1299.99, "Fourth parameter should be product price"
        
        print("\n✓ TEST 1 PASSED: Product write operation successful")
        print(f"  - Inserted product: {test_product.name}")
        print(f"  - Product ID: {test_id}")
        print(f"  - Query executed: INSERT INTO store_manager.products")

    def test_select_all_products(self, product_dao, mock_cassandra_connection):
        """
        TEST 2: READ OPERATION
        
        Tests that all products are correctly retrieved from Cassandra.
        Verifies:
        - The correct SELECT query is executed
        - Results are properly formatted as a list of dictionaries
        - All product fields are included in the response
        """
        # Arrange - Create mock database results
        mock_cluster, mock_session = mock_cassandra_connection
        
        # Simulate Cassandra row objects
        mock_row1 = MagicMock()
        mock_row1.name = "Laptop"
        mock_row1.sku = "LAP-001"
        mock_row1.price = 999.99
        
        mock_row2 = MagicMock()
        mock_row2.name = "Wireless Mouse"
        mock_row2.sku = "MOU-002"
        mock_row2.price = 29.99
        
        mock_row3 = MagicMock()
        mock_row3.name = "USB-C Cable"
        mock_row3.sku = "CAB-003"
        mock_row3.price = 12.50
        
        # Configure mock to return these rows
        mock_session.execute.return_value = [mock_row1, mock_row2, mock_row3]

        # Act - Retrieve all products
        results = product_dao.select_all()

        # Assert - Verify the database interaction and results
        # Check that execute was called
        assert mock_session.execute.call_count == 1, \
            "session.execute should be called exactly once"
        
        # Get the query
        call_args = mock_session.execute.call_args[0]
        query = call_args[0]
        
        # Verify the query structure
        assert "SELECT" in query.upper(), \
            "Query should be a SELECT statement"
        assert "FROM store_manager.products" in query, \
            "Query should select from store_manager.products table"
        
        # Verify the results format and content
        assert isinstance(results, list), \
            "Results should be a list"
        assert len(results) == 3, \
            f"Should return 3 products, got {len(results)}"
        
        # Verify first product
        assert results[0]["name"] == "Laptop"
        assert results[0]["sku"] == "LAP-001"
        assert results[0]["price"] == 999.99
        
        # Verify second product
        assert results[1]["name"] == "Wireless Mouse"
        assert results[1]["sku"] == "MOU-002"
        assert results[1]["price"] == 29.99
        
        # Verify third product
        assert results[2]["name"] == "USB-C Cable"
        assert results[2]["sku"] == "CAB-003"
        assert results[2]["price"] == 12.50
        
        print("\n✓ TEST 2 PASSED: Product read operation successful")
        print(f"  - Retrieved {len(results)} products")
        print(f"  - Products: {[r['name'] for r in results]}")
        print(f"  - Query executed: SELECT * FROM store_manager.products")


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])