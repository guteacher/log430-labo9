import pytest
import requests
import time


class TestProductAPISmoke:
    
    BASE_URL = "http://localhost:5000"
    
    @pytest.fixture(scope="class")
    def api_health_check(self):
        try:
            requests.get(f"{self.BASE_URL}/products", timeout=5)
            return True
        except requests.exceptions.ConnectionError:
            pytest.fail(f"API is not running at {self.BASE_URL}")
        except Exception as e:
            pytest.fail(f"Error connecting to API: {str(e)}")
    
    def test_01_api_is_running(self):
        response = requests.get(f"{self.BASE_URL}/products")
        assert response.status_code in [200, 404]
    
    def test_02_create_product(self):
        test_product = {
            "name": "Cheap Laptop",
            "sku": f"LAPTOP-{int(time.time())}",
            "price": 999.95
        }
        
        response = requests.post(
            f"{self.BASE_URL}/products",
            json=test_product,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code in [200, 201]
    
    def test_03_get_products(self):
        response = requests.get(f"{self.BASE_URL}/products")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, (list, dict))
    
    def test_04_create_and_retrieve(self):
        unique_sku = f"SMOKE-{int(time.time())}"
        test_product = {
            "name": "Gamer Mouse",
            "sku": unique_sku,
            "price": 29.99
        }
        
        create_response = requests.post(
            f"{self.BASE_URL}/products",
            json=test_product,
            headers={"Content-Type": "application/json"}
        )
        assert create_response.status_code in [200, 201]
        
        time.sleep(2)
        
        get_response = requests.get(f"{self.BASE_URL}/products")
        assert get_response.status_code == 200
        
        products = get_response.json()
        if isinstance(products, dict) and 'products' in products:
            products = products['products']
        
        assert isinstance(products, list)
        
        found = False
        for product in products:
            if product.get('sku') == unique_sku:
                found = True
                assert product['name'] == test_product['name']
                assert float(product['price']) == test_product['price']
                break
        
        assert found, f"Product with SKU {unique_sku} not found"
    
    def test_05_invalid_data(self):
        invalid_product = {"name": "Incomplete Product"}
        
        response = requests.post(
            f"{self.BASE_URL}/products",
            json=invalid_product,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code >= 400

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
