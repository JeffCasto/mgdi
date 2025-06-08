import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db.config import Base, get_db
from app.db.memory import MemoryEntry

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

@pytest.fixture
def client():
    """Test client with in-memory DB"""
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        # TODO: Use async test DB for pgvector tests
        pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_memory_store(client):
    """Test vector memory storage"""
    response = client.post("/api/memory/store", json={
        "content": "User prefers dark theme",
        "metadata": {"type": "preference"}
    })
    # TODO: Mock OpenAI embedding call
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["content"] == "User prefers dark theme"

def test_memory_search(client):
    """Test vector similarity search"""
    # TODO: Setup test memories with known embeddings
    response = client.get("/api/memory/search?query=theme preferences")
    assert response.status_code == 200
    # TODO: Assert similarity scoring

def test_memory_timeline(client):
    """Test chronological timeline fetch"""
    response = client.get("/api/memory/timeline")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_auth_gated_memory_access(client):
    """Test memory isolation by user"""
    # TODO: Test JWT-based user isolation
    # TODO: Verify user A cannot access user B's memories
    pass

@pytest.mark.asyncio
async def test_vector_similarity():
    """Test pgvector similarity calculation"""
    # TODO: Test actual vector distance calculations
    # TODO: Verify embedding dimensions match model
    pass
