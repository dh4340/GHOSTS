import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.mark.parametrize(
    "method, endpoint",
    [
        ("get", "/binary"),
        ("post", "/binary"),
    ],
)
def test_return_binary_without_file_name(method, endpoint):
    """Test binary file generation without a file name (GET and POST)."""
    response = getattr(client, method)(endpoint)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "method, endpoint, file_extension",
    [
        ("get", "/binary/{mock_file_name}", "bin"),
        ("post", "/binary/{mock_file_name}", "bin"),
    ],
)
def test_return_binary_with_file_name(method, endpoint, file_extension, mock_file_name):
    """Test binary file generation with a file name (GET and POST)."""
    response = getattr(client, method)(endpoint + mock_file_name(file_extension))
    assert response.status_code == 200
