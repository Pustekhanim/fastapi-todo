import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def auth_headers():
    # Register user
    user_data = {
        "username": "testuser",
        "password": "testpass",
        "first_name": "Test"
    }
    client.post("/signup", json=user_data)
    
    # Login and get token
    login_data = {
        "username": "testuser",
        "password": "testpass"
    }
    response = client.post("/token", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_register_login():
    # Test registration
    response = client.post("/signup", json={
        "username": "newuser",
        "password": "newpass123",
        "first_name": "New",
        "last_name": "User"
    })
    assert response.status_code == 200
    
    # Test login
    response = client.post("/token", data={
        "username": "newuser",
        "password": "newpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_task_crud_operations(auth_headers):
    # Create task
    task_data = {"title": "Test Task", "description": "Test Description"}
    response = client.post("/tasks", json=task_data, headers=auth_headers)
    assert response.status_code == 200
    task_id = response.json()["id"]
    
    # Get task
    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"
    
    # Update task
    update_data = {"title": "Updated Task"}
    response = client.put(f"/tasks/{task_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    
    # Delete task
    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200

def test_task_status_operations(auth_headers):
    # Create task
    response = client.post("/tasks", json={"title": "Status Test"}, headers=auth_headers)
    task_id = response.json()["id"]
    
    # Mark as completed
    response = client.put(f"/tasks/{task_id}/complete", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["status"] == "Completed"
    
    # Filter by status
    response = client.get("/tasks?status=Completed", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_pagination(auth_headers):
    # Create multiple tasks
    for i in range(3):
        client.post("/tasks", json={"title": f"Task {i}"}, headers=auth_headers)
    
    # Test pagination
    response = client.get("/tasks?skip=1&limit=2", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_unauthorized_access():
    # Try to access protected endpoint without token
    response = client.get("/tasks")
    assert response.status_code == 401
    
    # Try with invalid token
    response = client.get("/tasks", headers={"Authorization": "Bearer invalid"})
    assert response.status_code == 401