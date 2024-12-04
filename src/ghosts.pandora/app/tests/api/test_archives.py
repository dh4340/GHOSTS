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
    "method, endpoint",
    [
        ("get", "/zip/{mock_file_name}"),
        ("post", "/zip/{mock_file_name}"),
    ],
)
def test_zip_with_filename(method, endpoint, mock_file_name):
    response = getattr(client, method)(endpoint.format(mock_file_name=mock_file_name))
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
    "method, endpoint",
    [
        ("get", "/tar/{mock_file_name}"),
        ("post", "/tar/{mock_file_name}"),
    ],
)
def test_tar_with_filename(method, endpoint, mock_file_name):
    response = getattr(client, method)(endpoint.format(mock_file_name=mock_file_name))
    assert response.status_code == 200
