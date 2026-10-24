
import os
from types import SimpleNamespace

os.environ.setdefault("SECRET_KEY", "test-only-secret-key")

import app as app_module
import pytest


@pytest.fixture
def flask_client():
    app_module.app.config.update(TESTING=True)

    with app_module.app.test_client() as test_client:
        yield test_client


def test_home_redirects_to_register(flask_client):
    response = flask_client.get("/")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/register")


def test_register_page_loads(flask_client):
    response = flask_client.get("/register")

    assert response.status_code == 200


def test_login_page_loads(flask_client):
    response = flask_client.get("/login")

    assert response.status_code == 200


def test_health_endpoint(flask_client):
    response = flask_client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_session_requires_bearer_token(flask_client):
    response = flask_client.post("/session")

    assert response.status_code == 401
    assert "error" in response.get_json()


def test_valid_mocked_firebase_login(flask_client, monkeypatch):
    monkeypatch.setattr(
        app_module,
        "verify_firebase_token",
        lambda token: {"uid": "test-user"}
    )

    monkeypatch.setattr(
        app_module.auth,
        "get_user",
        lambda uid: SimpleNamespace(
            uid=uid,
            display_name="Test User",
            email="test@example.com"
        )
    )

    response = flask_client.post(
        "/session",
        headers={"Authorization": "Bearer test-token"}
    )

    assert response.status_code == 200
    assert response.get_json() == {"success": True}

    # Check that the login session was created.
    with flask_client.session_transaction() as session:
        assert session["user_id"] == "test-user"
        assert session["user_name"] == "Test User"
