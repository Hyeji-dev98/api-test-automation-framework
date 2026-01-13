# utils/test_data.py

class TestData:
    #상품 관련 테스트 데이터
    VALID_PRODUCT = {
        "title": "Test Product",
        "price": 99.99,
        "description": "This is a test product",
        "image": "https://i.pravatar.cc",
        "category": "electronics"
    }

    # 장바구니 관련 테스트 데이터
    VALID_CART = {
        "userId": 1,
        "date": "2026-01-13",
        "products": [
            {"productId": 1, "quantity": 2},
            {"productId": 2, "quantity": 1}
        ]
    }
   # 사용자 관련 테스트 데이터
    USERS = [
        {
            "id": 1,
            "username": "johnd",
            "email": "john@gmail.com",
            "password": "m38rmF$",
            "name": {"firstname": "John", "lastname": "Doe"},
            "address": {
                "city": "kilcoole",
                "street": "new road",
                "number": 7682,
                "zipcode": "12926-3874"
            },
            "phone": "1-570-236-7033"
        },
        {
            "id": 2,
            "username": "user2",
            "email": "user2@example.com",
            "password": "password2",
            "name": {"firstname": "Jane", "lastname": "Smith"},
            "address": {
                "city": "Los Angeles",
                "street": "Sunset Blvd",
                "number": 456,
                "zipcode": "90001"
            },
            "phone": "987-654-3210"
        }
    ]

    # ✅ 실제 존재하는 사용자 (조회용)
    EXISTING_USER = {
        "id": 1,
        "username": "johnd"
    }

    # ✅ FakeStore 로그인 전용 계정 (공식)
    LOGIN_USER = {
        "username": "mor_2314",
        "password": "83r5^_"
    }


    # 새 사용자 생성용 샘플
    VALID_USER = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword",
        "name": {"firstname": "New", "lastname": "User"},
        "address": {
            "city": "Seoul",
            "street": "Gangnam",
            "number": 10,
            "zipcode": "06100"
        },
        "phone": "010-1234-5678"
    }


    @classmethod
    def get_test_user(cls, username):
        """username으로 사용자 조회"""
        for user in cls.USERS:
            if user["username"] == username:
                return user
        return None