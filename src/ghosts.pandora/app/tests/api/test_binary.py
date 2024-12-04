import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Mock data for testing
mock_binary_data = b"Random binary data"
mock_file_name = "test_file.bin"


@pytest.mark.parametrize("method", ["get", "post"])
def test_return_binary_without_file_name(
    method,
    mock_random_name,
):
    """Test binary file generation without a file name (GET and POST)."""
    mock_random_name.return_value = mock_file_name

    response = getattr(client, method)("/binary")
    assert response.status_code == 200


@pytest.mark.parametrize("method", ["get", "post"])
def test_return_binary_with_file_name(method):
    """Test binary file generation with a file name (GET and POST)."""

    response = getattr(client, method)(f"/binary/{mock_file_name}")
    assert response.status_code == 200
