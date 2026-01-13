# api-test-automation-framework
Python-based API test automation framework for E-commerce platform
# API Test Automation Framework

## 📌 프로젝트 개요
이 프로젝트는 **FakeStore API**를 대상으로 한 **자동화 API 테스트 프레임워크**입니다.  
테스트 대상은 상품, 장바구니, 사용자 관련 API이며, **Pytest 기반**으로 작성되었습니다.

주요 특징:
- 단위 테스트(Unit Test) 및 엔드투엔드 테스트(E2E) 지원
- RESTful API (GET, POST, PUT, DELETE) 테스트 지원
- 데이터 유효성 검증
- 성능/응답 시간 검증
- HTML 테스트 리포트 생성
- CI/CD 환경 연동 가능 (Jenkins / GitHub Actions)

### 기술 스택
- **Python 3.8+**
- **requests**: HTTP 요청 처리
- **pytest**: 테스트 프레임워크
- **pytest-html**: HTML 리포트 생성

---
### 설치 방법

1. Repository 클론
```bash
git clone https://github.com/Hyeji-dev98/api-test-automation-framework.git
cd api-test-automation-framework
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv

# Windows
venv\Scripts\activate

```

3. 필요한 라이브러리 설치
```bash
pip install -r requirements.txt
```

## 📖 사용 방법

### 전체 테스트 실행
```bash
pytest tests/ -v
```

### HTML 리포트 생성
```bash
pytest tests/ -v --html=reports/report.html --self-contained-html
```

### 특정 테스트 클래스만 실행
```bash
pytest tests/test_cart.py
```


## 📁 디렉토리 구조
api-test-automation-framework/
├── config/
│   ├── __init__.py
│   └── config.py          # API URL, 환경 설정
├── tests/
│   ├── __init__.py
│   ├── test_products.py   # 상품 API 테스트
│   ├── test_cart.py       # 장바구니 API 테스트
│   ├── test_users.py      # 사용자 API 테스트
│   └── test_e2e_flow.py   # E2E 사용자 구매 플로우 테스트
├── utils/
│   ├── __init__.py
│   ├── api_client.py      # API 호출 공통 함수
│   └── test_data.py       # 테스트 데이터
├── reports/               # 테스트 리포트
│   ├── report.html        # Pytest HTML 리포트
│   ├── allure-results/    # Allure raw 결과
│   └── allure-report/     # Allure HTML 리포트
├── requirements.txt       # Python 의존성
└── README.md

##  테스트 구성

1. Products API
 - 전체 상품 조회
 - 단일 상품 조회
 - 카테고리별 상품 조회
 - 가격/평점 검증
 - 성능 검증 (응답 시간)

2. Cart API
 - 전체 장바구니 조회
 - 특정 장바구니 조회
 - 사용자별 장바구니 조회
 - 장바구니 생성/수정/삭제
 - 수량 및 상품 데이터 무결성 검증

3. Users API
 - 사용자 조회
 - 사용자 생성/수정/삭제
 - 로그인 및 인증 검증
 - 패스워드/이메일 유효성 검증

4. E2E Flow
 - 사용자 로그인 → 상품 조회 → 장바구니 생성 → 장바구니 검증
 - 전체 구매 플로우 테스트