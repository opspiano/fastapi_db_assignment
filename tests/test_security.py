import pytest
from pydantic import ValidationError
from app.security import hash_password, verify_password
from app.schemas import UserCreate

def test_password_hashing():
    raw_password = "SecurePassword123!"
    hashed = hash_password(raw_password)
    
    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_password_unique_salt():
    raw_password = "SamePassword123"
    hash1 = hash_password(raw_password)
    hash2 = hash_password(raw_password)
    
    assert hash1 != hash2

def test_invalid_email_validation():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="invalid-email-format",
            password="password123"
        )
