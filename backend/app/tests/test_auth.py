import pytest
from app.core.security import hash_password, verify_password
from app.schemas.auth import UserCreate
from app.models import User

@pytest.mark.asyncio
async def test_password_hashing():
    password = "StrongPass123!"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("WrongPass", hashed)

@pytest.mark.asyncio
async def test_register_login_logout(client):
    user_data = {"email": "testuser@example.com", "password": "StrongPass123!"}

    # Register user
    res = await client.post("/api/v1/auth/register", json=user_data)
    assert res.status_code == 201
    user = res.json()
    assert user["email"] == user_data["email"]
    assert "id" in user
    assert user["is_active"] is True
    assert user["is_admin"] is False

    # Duplicate registration should fail
    res = await client.post("/api/v1/auth/register", json=user_data)
    assert res.status_code == 400
    assert "already registered" in res.text

    # Login with correct credentials
    res = await client.post("/api/v1/auth/login", json=user_data)
    assert res.status_code == 200
    assert "set-cookie" in res.headers
    cookie = res.headers.get("set-cookie")
    assert "access_token" in cookie

    # Access protected /me endpoint using cookie
    cookies = res.cookies
    res = await client.get("/api/v1/auth/me", cookies=cookies)
    assert res.status_code == 200
    current_user = res.json()
    assert current_user["email"] == user_data["email"]

    # Login with wrong password fails
    wrong_login = {"email": user_data["email"], "password": "WrongPassword!"}
    res = await client.post("/api/v1/auth/login", json=wrong_login)
    assert res.status_code == 401

    # Logout clears cookie
    res = await client.post("/api/v1/auth/logout", cookies=cookies)
    assert res.status_code == 200
    # After logout, accessing /me should fail
    res = await client.get("/api/v1/auth/me", cookies=cookies)
    assert res.status_code == 401