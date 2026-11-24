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
    assert res.status_code == 201
    data = res.json()
    assert data["username"] == "testuser12"
    assert "password" not in data
    assert "password_hash" not in data

    login_res = client.post(
        "/users/login",
        json={"username": "testuser12", "password": "mypassword123"},
    )
    assert login_res.status_code == 200
    assert login_res.json()["message"] == "Login successful"


def test_login_wrong_password():
    res = client.post(
        "/users/login",
        json={"username": "testuser12", "password": "wrongpassword"},
    )
    assert res.status_code == 401


def test_calculation_bread():
    add_res = client.post(
        "/calculations",
        json={"a": 10, "b": 5, "type": "Add"},
    )
    assert add_res.status_code == 201
    calc = add_res.json()
    calc_id = calc["id"]
    assert calc["result"] == 15.0

    browse_res = client.get("/calculations")
    assert browse_res.status_code == 200
    assert len(browse_res.json()) >= 1

    read_res = client.get(f"/calculations/{calc_id}")
    assert read_res.status_code == 200
    assert read_res.json()["id"] == calc_id

    edit_res = client.put(
        f"/calculations/{calc_id}",
        json={"a": 20, "b": 4, "type": "Divide"},
    )
    assert edit_res.status_code == 200
    assert edit_res.json()["result"] == 5.0

    del_res = client.delete(f"/calculations/{calc_id}")
    assert del_res.status_code == 204

    get_deleted = client.get(f"/calculations/{calc_id}")
    assert get_deleted.status_code == 404


def test_calculation_invalid_inputs():
    zero_res = client.post(
        "/calculations",
        json={"a": 10, "b": 0, "type": "Divide"},
    )
    assert zero_res.status_code == 422

    bad_type = client.post(
        "/calculations",
        json={"a": 10, "b": 2, "type": "Unknown"},
    )
    assert bad_type.status_code == 422

    not_found = client.get("/calculations/999999")
    assert not_found.status_code == 404
