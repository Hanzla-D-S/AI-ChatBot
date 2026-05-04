import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

with patch("backend.rag_pipeline.load_rag_chain"):
    from backend.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "running" in response.json()["status"]


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_chat_empty_message():
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 400


def test_chat_valid_message():
    with patch("backend.main.get_response", return_value="You can track your order in My Orders section."):
        response = client.post("/chat", json={"message": "How do I track my order?"})
        assert response.status_code == 200
        assert "reply" in response.json()
        assert len(response.json()["reply"]) > 0


def test_chat_response_structure():
    with patch("backend.main.get_response", return_value="Test reply"):
        response = client.post("/chat", json={"message": "What is your return policy?"})
        data = response.json()
        assert "reply" in data
        assert isinstance(data["reply"], str)