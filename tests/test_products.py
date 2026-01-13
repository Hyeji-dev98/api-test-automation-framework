# tests/test_products.py
import pytest
from utils.api_client import APIClient
from utils.test_data import TestData
from config.config import Config

class TestProductAPI:

    @classmethod
    def setup_class(cls):
        cls.client = APIClient()

    @classmethod
    def teardown_class(cls):
        cls.client.close()
    # 전체 상품 목록 조회 상태 코드 확인
    #/products 호출 시 HTTP 상태 코드가 200 OK인지 확인
    def test_get_all_products_status_code(self):
        response = self.client.get("/products")
        assert response.status_code == 200

    # 전체 상품 목록 응답 구조 확인
    def test_get_all_products_response_structure(self):
        response = self.client.get("/products")
        products = response.json()
        assert isinstance(products, list)
        assert len(products) > 0
        first_product = products[0]
        required_fields = ['id', 'title', 'price', 'category', 'description', 'image', 'rating']
        for field in required_fields:
            assert field in first_product
    # 단일 상품 조회 성공
    def test_get_single_product_success(self):
        product_id = 1
        response = self.client.get(f"/products/{product_id}")
        assert response.status_code == 200
        product = response.json()
        assert product['id'] == product_id
    # 존재하지 않는 상품 조회
    def test_get_single_product_not_found(self):
        invalid_product_id = 99999
        response = self.client.get(f"/products/{invalid_product_id}")

        # FakeStore API는 존재하지 않는 상품 조회 시 200 OK와 빈 바디 반환
        assert response.status_code == 200

        # 빈 바디 처리
        if response.text.strip() == "":
            product = None
        else:
            product = response.json()

        assert product is None
    # 카테고리별 상품 조회
    def test_get_products_by_category(self):
        category = "electronics"
        response = self.client.get(f"/products/category/{category}")
        assert response.status_code == 200
        products = response.json()
        assert isinstance(products, list)
        assert all([p['category'] == category for p in products])
    # 전체 카테고리 목록 조회
    def test_get_all_categories(self):
        response = self.client.get("/products/categories")
        assert response.status_code == 200
        categories = response.json()
        expected_categories = ['electronics', 'jewelery', "men's clothing", "women's clothing"]
        for cat in expected_categories:
            assert cat in categories
    # 상품 가격 데이터 유효성 검증
    def test_product_price_validation(self):
        response = self.client.get("/products")
        products = response.json()
        for product in products:
            price = product['price']
            assert isinstance(price, (int, float))
            assert price > 0
            assert price <= Config.VALIDATION_RULES['price']['max']
    # 상품 평점 데이터 유효성 검증
    def test_product_rating_validation(self):
        response = self.client.get("/products")
        products = response.json()
        for product in products:
            rating = product['rating']
            assert 'rate' in rating
            assert 'count' in rating
            assert 0 <= rating['rate'] <= 5
            assert rating['count'] >= 0
    # 상품 조회 API 응답 시간
    def test_product_response_time(self):
        response, elapsed = self.client.measure_response_time('GET', '/products')
        assert response.status_code == 200
        assert elapsed < Config.PERFORMANCE_THRESHOLD['response_time']
