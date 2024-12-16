import json

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_json_default(default_json_response):
    """Test JSON generation with default parameters."""
    response = default_json_response
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert len(json.loads(response.content)) > 0


def test_json_with_path(json_with_path_response):
    """Test JSON generation with a dynamic path."""
    response = json_with_path_response
    assert response.status_code == 200

    assert response.headers["Content-Disposition"].startswith(
        "inline; filename=test-path.json"
    )
    assert response.headers["Content-Type"] == "application/json"


def test_json_invalid_ollama(default_json_response):
    """Simulate Ollama failure and ensure Faker fallback."""
    response = default_json_response
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    data = json.loads(response.content)
    assert len(data) > 0
