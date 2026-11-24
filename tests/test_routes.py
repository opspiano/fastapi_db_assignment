import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield


def test_register_and_login():
    res = client.post(
        "/users/register",
        json={
            "username": "testuser12",
            "email": "testuser12@example.com",
            "password": "mypassword123",
        },
    )
    assert res.status_code == 200

    login_res = client.post(
        "/users/login",
        json={"username": "testuser12", "password": "mypassword123"},
    )
    assert login_res.status_code == 200


def test_calculation_bread():
    add_res = client.post(
        "/calculations",
        json={"a": 10, "b": 5, "type": "Add"},
    )
    assert add_res.status_code == 200
    calc_id = add_res.json()["id"]

    read_res = client.get(f"/calculations/{calc_id}")
    assert read_res.status_code == 200
