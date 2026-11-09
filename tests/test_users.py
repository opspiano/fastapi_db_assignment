import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield

def test_create_user_and_check_response():
    response = client.post(
        "/users/",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secretpassword"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data
    assert "password_hash" not in data
    assert "password" not in data

def test_create_duplicate_user():
    response = client.post(
        "/users/",
        json={
            "username": "alice",
            "email": "alice_different@example.com",
            "password": "secretpassword"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username or email already registered"

def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
