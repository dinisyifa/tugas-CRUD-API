import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ======= FIXTURES =======
@pytest.fixture(scope="module")
def sample_user():
    return {
        "username": "dinisyifa28",
        "email": "dinisyifa28@mail.com",
        "password": "Password@123",
        "role": "staff"
    }

@pytest.fixture(scope="module")
def admin_user():
    return {
        "username": "adminuser",
        "email": "admin@mail.com",
        "password": "Admin@123",
        "role": "admin"
    }

# ======= TESTS =======
def test_create_user(sample_user):
    response = client.post("/users", json=sample_user)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == sample_user["username"]
    assert data["email"] == sample_user["email"]
    assert data["role"] == "staff"

def test_create_admin(admin_user):
    response = client.post("/users", json=admin_user)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == admin_user["username"]
    assert data["role"] == "admin"

def test_read_all_users_as_admin():
    response = client.get("/users?role=admin")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(user["role"] == "admin" for user in data)

def test_read_all_users_as_staff_forbidden():
    response = client.get("/users?role=staff")
    assert response.status_code == 403
    assert response.json()["detail"] == "Only admin can view all users"

def test_update_user_as_admin(sample_user):
    users = client.get("/users?role=admin").json()
    user_id = users[0]["id"]

    new_data = {
        "username": "dinisyifa",
        "email": "dinisyifa@mail.com",
        "password": "NewPass@123",
        "role": "staff"
    }
    response = client.put(f"/users/{user_id}?role=admin", json=new_data)
    assert response.status_code == 200
    updated = response.json()
    assert updated["username"] == "dinisyifa"
    assert updated["email"] == "dinisyifa@mail.com"

def test_update_user_as_staff_forbidden(sample_user):
    users = client.get("/users?role=admin").json()
    user_id = users[0]["id"]

    new_data = {
        "username": "forbiddenuser",
        "email": "forbidden@mail.com",
        "password": "Forbidden@123",
        "role": "staff"
    }
    response = client.put(f"/users/{user_id}?role=staff", json=new_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Only admin can update users"

def test_delete_user_as_admin():
    users = client.get("/users?role=admin").json()
    user_id = users[-1]["id"]

    response = client.delete(f"/users/{user_id}?role=admin")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"

def test_delete_user_as_staff_forbidden():
    users = client.get("/users?role=admin").json()
    user_id = users[0]["id"]

    response = client.delete(f"/users/{user_id}?role=staff")
    assert response.status_code == 403
    assert response.json()["detail"] == "Only admin can delete users"