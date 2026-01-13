"""
User API Test Cases
사용자 API 테스트 케이스
"""

import pytest
from utils.api_client import APIClient
from utils.test_data import TestData


class TestUserAPI:
    """사용자 API 테스트 케이스"""
    
    @classmethod
    def setup_class(cls):
        """테스트 클래스 실행 전 1회 실행"""
        cls.client = APIClient()
    
    @classmethod
    def teardown_class(cls):
        """테스트 클래스 종료 후 1회 실행"""
        cls.client.close()
    
    def test_get_all_users(self):
        """
        TC-023: 전체 사용자 조회
        Expected: 200 OK, 사용자 목록 반환
        """
        response = self.client.get("/users")
        
        assert response.status_code == 200, \
            f"Expected 200, but got {response.status_code}"
        
        users = response.json()
        assert isinstance(users, list), "Response should be a list"
        assert len(users) > 0, "User list should not be empty"
    
    def test_get_single_user(self):
        """
        TC-024: 특정 사용자 조회
        Expected: 사용자 상세 정보 반환
        """
        user_id = 1
        response = self.client.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        
        user = response.json()
        assert user['id'] == user_id, \
            f"Expected user id {user_id}, but got {user['id']}"
        
        # 필수 필드 검증
        required_fields = ['email', 'username', 'name', 'address', 'phone']
        for field in required_fields:
            assert field in user, f"Required field '{field}' is missing"
        
        # name 객체 내부 필드 검증
        assert 'firstname' in user['name'], "firstname is missing in name"
        assert 'lastname' in user['name'], "lastname is missing in name"
        
        # address 객체 내부 필드 검증
        assert 'city' in user['address'], "city is missing in address"
        assert 'street' in user['address'], "street is missing in address"
    
    def test_user_email_format_validation(self):
        """
        TC-025: 사용자 이메일 형식 검증
        실무: 이메일 유효성 검증
        Expected: 이메일 형식이 유효
        """
        response = self.client.get("/users")
        users = response.json()
        
        for user in users:
            email = user['email']
            
            # 이메일이 문자열인지 확인
            assert isinstance(email, str), \
                f"User {user['id']}: Email should be string"
            
            # 이메일에 @ 포함 여부 확인
            assert '@' in email, \
                f"User {user['id']}: Invalid email format (missing @): {email}"
            
            # @ 뒤에 도메인이 있는지 확인
            email_parts = email.split('@')
            assert len(email_parts) == 2, \
                f"User {user['id']}: Invalid email format: {email}"
            
            # 도메인에 . 포함 여부 확인
            domain = email_parts[1]
            assert '.' in domain, \
                f"User {user['id']}: Invalid email domain (missing .): {email}"
    
    def test_user_phone_format(self):
        """
        TC-026: 사용자 전화번호 형식 검증
        Expected: 전화번호가 문자열 형태로 존재
        """
        response = self.client.get("/users")
        users = response.json()
        
        for user in users:
            phone = user['phone']
            
            # 전화번호가 문자열인지 확인
            assert isinstance(phone, str), \
                f"User {user['id']}: Phone should be string"
            
            # 전화번호가 비어있지 않은지 확인
            assert len(phone) > 0, \
                f"User {user['id']}: Phone should not be empty"
    
    def test_user_address_structure(self):
        """
        TC-027: 사용자 주소 데이터 구조 검증
        실무: 복합 데이터 구조 검증
        Expected: 주소 객체가 필수 필드 포함
        """
        response = self.client.get("/users")
        users = response.json()
        
        required_address_fields = ['city', 'street', 'number', 'zipcode', 'geolocation']
        required_geo_fields = ['lat', 'long']
        
        for user in users:
            address = user['address']
            
            # 주소 필수 필드 확인
            for field in required_address_fields:
                assert field in address, \
                    f"User {user['id']}: Address missing field '{field}'"
            
            # geolocation 필드 확인
            geo = address['geolocation']
            for field in required_geo_fields:
                assert field in geo, \
                    f"User {user['id']}: Geolocation missing field '{field}'"
    
    def test_create_user_success(self):
        """
        TC-028: 사용자 생성 성공
        Expected: 생성된 사용자 정보 반환
        """
        new_user = TestData.VALID_USER.copy()
        
        response = self.client.post("/users", json=new_user)
        
        assert response.status_code in [200,201], \
            f"Expected 200, but got {response.status_code}"
        
        created_user = response.json()
        assert 'id' in created_user, "Created user should have an id"
        
        # 생성한 데이터가 응답에 포함되어 있는지 확인
        # FakeStore API는 실제로 저장하지 않고 응답만 반환
        # email, username 키가 있으면 비교, 없으면 패스
        if 'email' in created_user:
            assert created_user['email'] == new_user['email']
        if 'username' in created_user:
            assert created_user['username'] == new_user['username']
    
    def test_update_user_success(self):
        """
        TC-029: 사용자 정보 수정 성공
        Expected: 수정된 사용자 정보 반환
        """
        user_id = 1
        updated_data = {
            "email": "newemail@example.com",
            "username": "updateduser",
            "password": "newpassword123"
        }
        
        response = self.client.put(f"/users/{user_id}", json=updated_data)
        
        assert response.status_code == 200
        
        updated_user = response.json()
        assert updated_user['email'] == updated_data['email']
        assert updated_user['username'] == updated_data['username']
    
    
    def test_delete_user_success(self):
        """
        TC-031: 사용자 삭제 성공
        Expected: 200 OK
        """
        user_id = 1
        response = self.client.delete(f"/users/{user_id}")
        
        assert response.status_code == 200
    # 사용자 조회 테스트
    def test_get_user_success(self):
        user_id = TestData.EXISTING_USER["id"]

        response = self.client.get(f"/users/{user_id}")

        assert response.status_code == 200
        user = response.json()
        assert user["username"] == TestData.EXISTING_USER["username"]

    #로그인 테스트 (분리)
    def test_user_login_success(self):
        response = self.client.post("/auth/login", json=TestData.LOGIN_USER)

        assert response.status_code in [200,201]
        assert "token" in response.json()

    def test_user_login_invalid_credentials(self):
        """
        TC-033: 잘못된 인증 정보로 로그인 실패
        실무: 인증 실패 케이스 검증
        Expected: 401 Unauthorized
        """
        response = self.client.post("/auth/login", json={
            "username": "invaliduser",
            "password": "wrongpassword"
        })
        
        assert response.status_code == 401, \
            f"Expected 401 for invalid credentials, but got {response.status_code}"
    
    def test_user_login_missing_credentials(self):
        """
        TC-034: 인증 정보 누락 시 로그인 실패
        실무: 필수 파라미터 누락 케이스 검증
        Expected: 400 Bad Request 또는 401 Unauthorized
        """
        # username만 있고 password 누락
        response = self.client.post("/auth/login", json={
            "username": "johnd"
        })
        
        assert response.status_code in [400, 401], \
            f"Expected 400 or 401 for missing password, but got {response.status_code}"
    
    
    def test_user_not_found(self):
        """
        TC-037: 존재하지 않는 사용자 조회
        실무: 엣지 케이스 검증
        Expected: null 반환 또는 404
        """
        invalid_user_id = 99999
        response = self.client.get(f"/users/{invalid_user_id}")
        
        # FakeStore API는 존재하지 않는 사용자에 대해 null 반환
        assert response.status_code == 200
        assert response.json() is None, \
            "Non-existent user should return null"