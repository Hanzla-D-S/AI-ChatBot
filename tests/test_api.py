# import pytest
# from fastapi.testclient import TestClient
# from unittest.mock import patch

# with patch("backend.rag_pipeline.load_rag_chain"):
#     from backend.main import app

# client = TestClient(app)


# def test_root():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert "running" in response.json()["status"]


# def test_health_check():
#     response = client.get("/health")
#     assert response.status_code == 200
#     assert response.json() == {"status": "healthy"}


# def test_chat_empty_message():
#     response = client.post("/chat", json={"message": ""})
#     assert response.status_code == 400


# def test_chat_valid_message():
#     with patch("backend.main.get_response", return_value="You can track your order in My Orders section."):
#         response = client.post("/chat", json={"message": "How do I track my order?"})
#         assert response.status_code == 200
#         assert "reply" in response.json()
#         assert len(response.json()["reply"]) > 0


# def test_chat_response_structure():
#     with patch("backend.main.get_response", return_value="Test reply"):
#         response = client.post("/chat", json={"message": "What is your return policy?"})
#         data = response.json()
#         assert "reply" in data
#         assert isinstance(data["reply"], str)
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch, MagicMock

# Mock BEFORE importing anything from backend
mock_chain = MagicMock()
mock_chain.return_value = {"answer": "You can track your order in My Orders section."}

with patch("backend.rag_pipeline.load_rag_chain", return_value=mock_chain):
    with patch("backend.rag_pipeline.rag_chain", None):
        from backend.main import app

from fastapi.testclient import TestClient
client = TestClient(app)


def test_root():
    """Test root endpoint returns running status."""
    response = client.get("/")
    assert response.status_code == 200
    assert "running" in response.json()["status"]


def test_health_check():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_chat_empty_message():
    """Test that empty message returns 400 error."""
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 400


def test_chat_valid_message():
    """Test that a valid message returns a reply."""
    with patch("backend.main.get_response", return_value="You can track your order in My Orders."):
        response = client.post("/chat", json={"message": "How do I track my order?"})
        assert response.status_code == 200
        assert "reply" in response.json()


def test_chat_response_structure():
    """Test response has correct structure."""
    with patch("backend.main.get_response", return_value="Test reply"):
        response = client.post("/chat", json={"message": "What is your return policy?"})
        data = response.json()
        assert "reply" in data
        assert isinstance(data["reply"], str)