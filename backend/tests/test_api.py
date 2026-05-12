"""
Tests for the FastAPI JWT Authentication API.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def get_tokens(username: str = "admin", password: str = "admin123") -> dict:
    response = client.post(
        "/token",
        data={"username": username, "password": password},
    )
    return response


class TestLogin:
    def test_login_success(self):
        resp = get_tokens()
        assert resp.status_code == 200
        body = resp.json()
        assert "access_token" in body
        assert "refresh_token" in body
        assert body["token_type"] == "bearer"
        assert body["expires_in"] == 300

    def test_login_wrong_password(self):
        resp = get_tokens(password="wrongpassword")
        assert resp.status_code == 401

    def test_login_unknown_user(self):
        resp = get_tokens(username="nobody", password="whatever")
        assert resp.status_code == 401


class TestRefresh:
    def test_refresh_success(self):
        tokens = get_tokens().json()
        resp = client.post(
            "/token/refresh",
            json={"refresh_token": tokens["refresh_token"]},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "access_token" in body
        assert "refresh_token" in body
        assert body["expires_in"] == 300

    def test_refresh_with_access_token_fails(self):
        """Access tokens must not be accepted as refresh tokens."""
        tokens = get_tokens().json()
        resp = client.post(
            "/token/refresh",
            json={"refresh_token": tokens["access_token"]},
        )
        assert resp.status_code == 401

    def test_refresh_invalid_token(self):
        resp = client.post(
            "/token/refresh",
            json={"refresh_token": "not.a.valid.token"},
        )
        assert resp.status_code == 401


class TestProtectedEndpoint:
    def test_me_authenticated(self):
        tokens = get_tokens().json()
        resp = client.get(
            "/me",
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        assert resp.status_code == 200
        assert resp.json()["username"] == "admin"

    def test_me_unauthenticated(self):
        resp = client.get("/me")
        assert resp.status_code == 401

    def test_me_with_refresh_token_fails(self):
        """Refresh tokens must not grant access to protected endpoints."""
        tokens = get_tokens().json()
        resp = client.get(
            "/me",
            headers={"Authorization": f"Bearer {tokens['refresh_token']}"},
        )
        assert resp.status_code == 401
