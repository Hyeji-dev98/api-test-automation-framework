# tests/conftest.py
import pytest

@pytest.fixture
def common_headers():
    return {
        "User-Agent": "Mozilla/5.0 (GitHub Actions)",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
