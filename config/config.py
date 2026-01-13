"""
E-commerce API Test Configuration
FakeStore API를 사용한 테스트 환경 설정
"""


class Config:
    BASE_URL = "https://fakestoreapi.com"

    # 가격 검증 최대값
    VALIDATION_RULES = {
        "price": {"max": 1000}
    }

    # 성능 기준 (초)
    PERFORMANCE_THRESHOLD = {
        "response_time": 2  # 2초
    }