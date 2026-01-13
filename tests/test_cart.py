"""
Cart API Test Cases
장바구니 API 테스트 케이스 - 데이터 무결성 검증 반영
"""

import pytest
from utils.api_client import APIClient
from utils.test_data import TestData


class TestCartAPI:
    """장바구니 API 테스트 케이스"""
    
    @classmethod
    def setup_class(cls):
        """테스트 클래스 실행 전 1회 실행"""
        cls.client = APIClient()
    
    @classmethod
    def teardown_class(cls):
        """테스트 클래스 종료 후 1회 실행"""
        cls.client.close()
    
    def test_get_all_carts(self):
        """
        TC-014: 전체 장바구니 조회
        Expected: 200 OK, 장바구니 목록 반환
        """
        response = self.client.get("/carts")
        
        assert response.status_code == 200
        
        carts = response.json()
        assert isinstance(carts, list)
        assert len(carts) > 0
    
    def test_get_single_cart(self):
        """
        TC-015: 특정 장바구니 조회
        Expected: 장바구니 상세 정보 반환
        """
        cart_id = 1
        response = self.client.get(f"/carts/{cart_id}")
        
        assert response.status_code == 200
        
        cart = response.json()
        assert cart['id'] == cart_id
        assert 'userId' in cart
        assert 'date' in cart
        assert 'products' in cart
        assert isinstance(cart['products'], list)
    
    def test_get_user_carts(self):
        """
        TC-016: 특정 사용자의 장바구니 조회
        실무: 사용자별 장바구니 데이터 검증
        Expected: 해당 사용자의 장바구니만 반환
        """
        user_id = 1
        response = self.client.get(f"/carts/user/{user_id}")
        
        assert response.status_code == 200
        
        carts = response.json()
        assert isinstance(carts, list)
        
        # 모든 장바구니가 해당 사용자의 것인지 확인
        for cart in carts:
            assert cart['userId'] == user_id, \
                f"Expected userId {user_id}, but got {cart['userId']}"
    
    def test_create_cart_success(self):
        """
        TC-017: 장바구니 생성 성공
        실무: 장바구니 담기 기능 검증
        Expected: 생성된 장바구니 정보 반환
        """
        new_cart = TestData.VALID_CART.copy()
        
        response = self.client.post("/carts", json=new_cart)
        
        # 상태 코드 확인
        assert response.status_code in [200, 201]
        
        # 응답 body 최소 확인 (딕셔너리 형태인지)
        try:
            created_cart = response.json()
            assert isinstance(created_cart, dict)
        except Exception:
        # 응답이 비어있거나 JSON이 아니면 None 처리
            created_cart = None
        assert created_cart is not None
    
    def test_update_cart_success(self):
        """
        TC-018: 장바구니 수정 성공
        실무: 장바구니 수량 변경 검증
        Expected: 수정된 장바구니 정보 반환
        """
        cart_id = 1
        updated_cart = {
            "userId": 1,
            "date": "2024-01-13",
            "products": [
                {"productId": 1, "quantity": 5}  # 수량 변경
            ]
        }
        
        response = self.client.put(f"/carts/{cart_id}", json=updated_cart)
        
        assert response.status_code == 200
        
        result = response.json()
        assert result['userId'] == updated_cart['userId']
    
    def test_delete_cart_success(self):
        """
        TC-019: 장바구니 삭제 성공
        Expected: 200 OK
        """
        cart_id = 1
        response = self.client.delete(f"/carts/{cart_id}")
        
        assert response.status_code == 200
    
    def test_cart_product_data_integrity(self):
        """
        TC-020: 장바구니-상품 데이터 무결성 검증
        실무: Backoffice-Frontend 데이터 정합성 검증 경험 반영
        Expected: 장바구니의 상품 ID가 실제 존재하는 상품
        """
        # 1. 장바구니 조회
        cart_response = self.client.get("/carts/1")
        cart = cart_response.json()
        
        # 2. 장바구니의 각 상품이 실제로 존재하는지 확인
        for cart_product in cart['products']:
            product_id = cart_product['productId']
            
            # 해당 상품 조회
            product_response = self.client.get(f"/products/{product_id}")
            
            # 상품이 존재해야 함
            assert product_response.status_code == 200, \
                f"Product {product_id} in cart does not exist"
            
            product = product_response.json()
            assert product is not None, \
                f"Product {product_id} returned null"
    
    def test_cart_quantity_validation(self):
        """
        TC-021: 장바구니 수량 유효성 검증
        실무: 수량 데이터 검증
        Expected: 수량은 양의 정수
        """
        response = self.client.get("/carts")
        carts = response.json()
        
        for cart in carts:
            for product in cart['products']:
                quantity = product['quantity']
                
                # 수량이 정수인지 확인
                assert isinstance(quantity, int), \
                    f"Cart {cart['id']}: Quantity should be integer, got {type(quantity)}"
                
                # 수량이 양수인지 확인
                assert quantity > 0, \
                    f"Cart {cart['id']}: Quantity should be positive, got {quantity}"
    
    def test_get_carts_by_date_range(self):
        """
        TC-022: 날짜 범위로 장바구니 조회
        FakeStore API는 날짜 필터링 미지원 → 전체 조회
        Expected: 장바구니 리스트 반환
        """
        response = self.client.get("/carts")
        assert response.status_code == 200

        carts = response.json()
        assert isinstance(carts, list)