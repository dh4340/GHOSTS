import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.mark.parametrize(
    "method, endpoint",
    [
        ("get", "/zip"),
        ("post", "/zip"),
    ],
)
def test_zip_default(method, endpoint):
    response = getattr(client, method)(endpoint)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "method, endpoint, file_extension",
    [
        ("get", "/zip/{mock_file_name}", "zip"),
        ("post", "/zip/{mock_file_name}", "zip"),
    ],
)
def test_zip_with_filename(method, endpoint, file_extension, mock_file_name):
    """Test return ZIP file with filename."""
    response = getattr(client, method)(endpoint + mock_file_name(file_extension))
    assert response.status_code == 200


@pytest.mark.parametrize(
    "method, endpoint",
    [
        ("get", "/tar"),
        ("post", "/tar"),
    ],
)
def test_tar_default(method, endpoint):
    response = getattr(client, method)(endpoint)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "method, endpoint, file_extension",
    [
        ("get", "/tar/{mock_file_name}", "tar"),
        ("post", "/tar/{mock_file_name}", "tar"),
    ],
)
def test_tar_with_filename(method, endpoint, file_extension, mock_file_name):
    """Test return TAR file with filename."""
    response = getattr(client, method)(endpoint + mock_file_name(file_extension))
    assert response.status_code == 200
