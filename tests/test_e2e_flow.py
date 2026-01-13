"""
End-to-End Test
사용자 구매 플로우 E2E 테스트
FakeStore API 특성 반영: 상태 유지 X, 로그인 토큰 없음
"""

import pytest
from utils.api_client import APIClient
from utils.test_data import TestData


class TestE2EFlow:

    @classmethod
    def setup_class(cls):
        cls.client = APIClient()

    @classmethod
    def teardown_class(cls):
        cls.client.close()

    def test_user_purchase_flow(self):
        """
        TC-E2E-01: 사용자 구매 전체 흐름
        Flow:
        1. 사용자 정보 확인
        2. 상품 조회
        3. 장바구니 생성
        4. 장바구니 데이터 검증
        Note:
        FakeStore는 실제 DB 저장 X, 토큰 제공 X
        """

        # 1️⃣ 사용자 정보 확인
        test_user = TestData.USERS[0]
        assert "id" in test_user
        user_id = test_user["id"]

        # 2️⃣ 상품 목록 조회
        products_response = self.client.get("/products")
        assert products_response.status_code == 200

        products = products_response.json() or []
        assert isinstance(products, list)
        assert len(products) > 0

        selected_product = products[0]
        product_id = selected_product.get("id", 1)

        # 3️⃣ 장바구니 생성
        cart_payload = {
            "userId": user_id,
            "date": "2026-01-13",
            "products": [
                {"productId": product_id, "quantity": 1}
            ]
        }

        create_cart_response = self.client.post("/carts", json=cart_payload)
        assert create_cart_response.status_code in [200, 201]

        created_cart = create_cart_response.json() or {}
        assert created_cart, "장바구니 생성 응답이 비어있습니다"

        # 4️⃣ 장바구니 데이터 검증
        assert created_cart.get("userId", user_id) == user_id
        products_in_cart = created_cart.get("products", [])
        assert isinstance(products_in_cart, list)
        assert len(products_in_cart) == 1
        assert products_in_cart[0].get("productId", product_id) == product_id
        assert products_in_cart[0].get("quantity", 1) == 1

        # 5️⃣ 전체 플로우 로그
        print("✅ E2E Flow Passed: User purchase flow simulated successfully")
