import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_token
from app.core.config import settings
import time

def test_hash_and_verify():
    pw = "strong-password-123"
    h = hash_password(pw)
    assert verify_password(pw, h) is True
    assert verify_password("wrong", h) is False

def test_jwt_create_and_decode():
    token = create_access_token("user-id-123", expires_minutes=1)
    payload = decode_token(token)
    assert payload and payload.get("sub") == "user-id-123"
