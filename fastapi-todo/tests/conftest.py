import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)
