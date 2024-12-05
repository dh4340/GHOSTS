import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.mark.parametrize(
    "method, endpoint",
    [
        ("get", "/csv/test"),
        ("post", "/csv/test"),
    ],
)
def test_return_csv_with_ollama_enabled(method, endpoint):
    response = getattr(client, method)(endpoint)
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == 'inline; filename="test.csv"'


@pytest.mark.parametrize(
    "method, endpoint",
    [
        ("get", "/csv/test"),
        ("post", "/csv/test"),
    ],
)
def test_return_csv_with_ollama_disabled(method, endpoint):
    response = getattr(client, method)(endpoint)
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == 'inline; filename="test.csv"'


@pytest.mark.parametrize(
    "method, endpoint, file_extension",
    [
        ("get", "/csv/", "csv"),
        ("post", "/csv/", "csv"),
    ],
)
def test_return_csv_with_random_name(method, endpoint, file_extension, mock_file_name):
    """Test return CSV file with a random name based on file extension."""
    response = getattr(client, method)(endpoint + mock_file_name(file_extension))
    assert response.status_code == 200
    assert "Content-Disposition" in response.headers
    assert response.headers["Content-Disposition"].endswith(f'.{file_extension}"')
